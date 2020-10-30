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
    global buttonPin
    while True:
        if not GPIO.input(buttonPin):
            Url = "http://localhost:5000/api/light/setAttr"
            OnOff = "on" if light.function =="off" else "off"
            Data = {"Room": Room,
                    "Lights": [light.name],
                    "AttrKey": ["function", OnOff]
                    }
            requests.post(Url, Data)
        light.main()
        time.sleep(light.Speed)

    return(None)

#this function is used to measure temp and load of the pi.
def PiControl(rooms):
    startTime = time.time()
    while True:
        time.sleep(5)
        if time.time() - startTime > BACKUPTIME*3600:
            #copy all the database here
            startTime = time.time()
            backupDataBases()

        temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "")[0:4]
        load = psutil.cpu_percent()
        rooms['pi']['room'].json['temperature'] = temp
        rooms['pi']['room'].json['load'] = load
        rooms['pi']['room'].writeToDB()
        print(rooms['pi']['room'].json)
        time.sleep(55)

def backupDataBases():
    CWD = os.getcwd()
    SourceDir = CWD + "/DataBases/"
    DestDir = CWD + "/" + BACKUPPATH
    Files = os.listdir("DataBases")
    FilePaths = []
    for File in Files:
        FilePath = SourceDir + File
        if os.path.isfile(FilePath):
            shutil.copy(FilePath, DestDir + File)
            print("File {} copied to {}".format(FilePath, DestDir + File))
