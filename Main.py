import threading
import time
import os
import psutil
import sys
import RPi.GPIO as GPIO
import datetime

#import needed modules
from Config import rooms
from Website import dirk as WEB
import LED
import data

#set up button to turn on lights without phone
GPIO.setmode(GPIO.BCM)
buttonPin = 4
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

time.sleep(1) #give modules some time to initialize global variables

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
        time.sleep(5)
        temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "")[0:4]
        load = psutil.cpu_percent()
        rooms['pi']['room'].json['temp'] = temp
        rooms['pi']['room'].json['load'] = load
        rooms['pi']['room'].sensorData.insert({
            "time": str(datetime.datetime.now()),
            "data":{ "temp": temp,
                "load": load}
            })

        #create data plot from sensors for each room:
        for roomID in rooms:
            rooms[roomID]['room'].createFig()
        print(rooms['pi']['room'].json)
        time.sleep(55)

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

