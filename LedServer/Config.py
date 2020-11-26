from decouple import config


DB = "ledserver"
DBUser = config('DBUSER')
DBPassword = config('DBPASS')

DarkMode = True

TempKeys = ["tijd", "SetPoint", "Room"]
TempDBTable = "TempSettings"
TempDBKeys = [
            ["tijd", "TIME"],
            ["SetPoint", "FLOAT"],
            ["Room", "VARCHAR(500)"]
]

dataKeys = [["temperature", "FLOAT"], ["humidity", "FLOAT"], ["ldr", "FLOAT"], ["time", "VARCHAR(500)"], ["room", "VARCHAR(500)"]] #create the keys for rooms
