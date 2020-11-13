import os
import psutil
import time
import RPi.GPIO as GPIO
import shutil
import requests
from __main__ import BACKUPTIME, BACKUPPATH

#set up button to turn on lights without phone
GPIO.setmode(GPIO.BCM)
buttonPin = 4
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#this is the worker function, it will run the main method of the light object.
def Worker(Room, light):
    while True:

        light.main()
        time.sleep(light.Speed)

    return(None)

def buttonRead():
    while True:
        time.sleep(0.1)
        if not GPIO.input(buttonPin):
            States = requests.post("http://localhost:5000/api/light/getStatus", json={})
            States = States.json()
            for Room in States:
                for Light in States[Room]:
                    Url = "http://localhost:5000/api/light/setAttr"
                    OnOff = "on" if States[Room][Light]["Function"] =="off" else "off"
                    Data = {"Room": Room,
                            "Lights": [Light],
                            "AttrKey": ["function", OnOff]
                            }
                    print(Data)
                    requests.post(Url, json=Data)
            time.sleep(5)

#this function is used to measure temp and load of the pi.
def PiControl(rooms):
    while True:
        time.sleep(5)
        temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "")[0:4]
        load = psutil.cpu_percent()
        uptime = os.popen("uptime").readline()
        uptime = uptime[uptime.find("up ") + 3:uptime.find(" user") - 4]
        rooms['pi']['room'].json['temperature'] = temp
        rooms['pi']['room'].json['cpuload'] = load
        rooms['pi']['room'].json['uptime'] = uptime
        rooms['pi']['room'].writeToDB()
        print(rooms['pi']['room'].json)
        time.sleep(55)
