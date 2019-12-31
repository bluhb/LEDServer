import LED
import data

dataKeys = ["temp", "humid", "LDR"] #create the keys for rooms
rooms = {}

rooms = {
        "pi":{
            "room":data.room(name="pi", dataKeys=["temp", "load"])
            },
        "bed":{
            "room":data.room(name="bed", dataKeys=dataKeys),
            "lights":{
                "LedStrip":LED.Arduino(name ='bed',
                    serialPort = 'ttyUSB0',
                    room = 'livingroom',
                    master = {'room':'livingroom', 'light':'LedStrip'},
                    roomSensors = 'livingroom')
                }
            },
        "livingroom":{
            "room":data.room(name='livingroom', dataKeys=dataKeys),
            "lights":{
                "LedStrip":LED.APALedstrip(name = 'livingroom',
                    room = 'livingroom')
                # "LedStrip2":LED.Arduino(name ='bed',
                    # serialPort = 'ttyUSB0',
                    # room = 'livingroom',
                    # master = {'room':'livingroom', 'light':'LedStrip'},
                    # roomSensors = 'livingroom')

                }
            }
        }
