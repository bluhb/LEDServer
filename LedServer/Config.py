import LED
import data

dataKeys = [["temperature", "float"], ["humidity", "float"], ["ldr", "float"], ["time", "varchar"], ["room", "varchar"]] #create the keys for rooms
rooms = {}

BACKUPTIME = 6 #Time in hours how often the database should be backed up
BACKUPPATH = "./DataBases/BackUps/"

rooms = {
        "pi":{
            "room":data.room(name="pi", dataKeys=[["room", "varchar"], ["temperature", "integer"], ["load", "integer"]])
            },
        "bed":{
            "room":data.room(name="bed", dataKeys=dataKeys),
            "lights":{
                "LedStrip":LED.Arduino(name ='bed',
                    serialPort = 'ttyUSB0',
                    master = {'room':'livingroom', 'light':'LedStrip'},
                    roomSensors = 'livingroom')
                }
            },
        "livingroom":{
            "room":data.room(name='livingroom', dataKeys=dataKeys),
            "lights":{
                "LedStrip":LED.APALedstrip(name = 'livingroom',
                    )
                # "LedStrip2":LED.Arduino(name ='bed',
                    # serialPort = 'ttyUSB0',
                    # room = 'livingroom',
                    # master = {'room':'livingroom', 'light':'LedStrip'},
                    # roomSensors = 'livingroom')

                }
            },
        "livingroom2":{
            "room":data.room(name="livingroom2", dataKeys=dataKeys),
            "lights":{
                "LedStrip":LED.WiFiLight("LedStrip",
                    "192.168.1.235")
                }
            }
        }
