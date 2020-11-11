import LED
import data

dataKeys = [["temperature", "float"], ["humidity", "float"], ["ldr", "float"], ["time", "varchar(500)"], ["room", "varchar(500)"]] #create the keys for rooms
rooms = {}

BACKUPTIME = 6 #Time in hours how often the database should be backed up
BACKUPPATH = "./DataBases/BackUps/"

rooms = {
        "pi":{
            "room":data.room(name="pi", dataKeys=[["room", "varchar(500)"], ["temperature", "integer"], ["load", "integer"]])
            },
        "bed":{
            "room":data.room(name="bed", dataKeys=dataKeys),
            "lights":{
                "LedStrip":LED.Arduino(name ='LedStrip',
                    serialPort = 'ttyUSB0',
                    master = {'room':'livingroom', 'light':'Muur'},
                    roomSensors = 'livingroom')
                }
            },
        "livingroom":{
            "room":data.room(name='livingroom', dataKeys=dataKeys),
            "lights":{
                "Muur":LED.APALedstrip(name = 'Muur',
                    ColorCorrection={"H": -10, "S":0, "V":0}
                    ),
                "Bank":LED.WiFiLight(Name = "Bank",
                    IP_ADRESS = "bank.lights",
                    Master = {"room":"livingroom", "light":"Muur"},
                )
                }
            }
        }
