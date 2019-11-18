import threading
import time
import LED
import data
from Website import dirk as WEB
import os
import psutil
import sys

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
buttonPin = 4
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

dataKeys = ["temp", "humid", "LDR"] #create the keys for rooms
rooms = {}

time.sleep(1) #give modules some time to initialize global variables
#initialize the rooms, pi is used for the cpu temp and load of the pi
#In this part the rooms and lights are set up
rooms['pi'] = {
    "room":data.room(name='pi', dataKeys=["temp","load"])
    }

rooms['livingroom'] = {
        "room":data.room(name = 'livingroom',dataKeys = dataKeys),
        "lights":{
            "LedStrip":LED.APALedstrip(name = 'livingroom',
                room = 'livingroom')
            }
        }

rooms['bed'] = {
        "room":data.room(name = 'bed', dataKeys = dataKeys),
        "lights":{
            "LedStrip":LED.Arduino(name ='bed',
                serialPort = 'ttyUSB0',
                room = 'livingroom',
                master = {'room':'livingroom', 'light':'LedStrip'},
                roomSensors = 'livingroom')
            }
        }

#--------------------------------------------------------------------
for key in rooms:
    print(key + ' room is created')

#this is the worker function, it will run the main method of the light object.
def Worker(light):
    global buttonPin
    while True:
        if not GPIO.input(buttonPin):
            light.color_rgb = {'r':255, 'g':150, 'b':120}
            light.function = 'colorfill'
        light.main()
        time.sleep(light.wait)

    return(None)

#this function is used to measure temp and load of the pi.
def PiControl():
    while True:
        time.sleep(60)
        rooms['pi']['room'].json['temp'] = os.popen("vcgencmd measure_temp").readline().replace("temp=", "")
        rooms['pi']['room'].json['load'] = psutil.cpu_percent()
        print(rooms['pi']['room'].json)

#add and start all threads for every light and for the pi
threads = {}
threads['pi'] = threading.Thread(target = PiControl)
threads['pi'].daemon = True
threads['pi'].start()

for room in rooms:
    try:
        if "lights" in rooms[room]:
            for key, value in rooms[room]['lights'].items():
                threads[key] = threading.Thread(target = Worker, args = (value,))
                threads[key].daemon = True
                threads[key].start()
                print(room + " " + key + " started a new thread")
                time.sleep(0.5)
    except:
        pass

#initialize and start the server.
WEB.init()
WEB.app.run('0.0.0.0', 5000, False)

for keys in rooms:
    print(keys)
    if not keys == 'pi':
        for lights in rooms[keys]['lights']:
            rooms[keys]['lights'][lights].exit()

print('closed everything')

