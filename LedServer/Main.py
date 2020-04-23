import threading
import time
import sys
import datetime


#import needed modules
import Error #Needs to be imported first, other module need this in the main
ErrorDB = Error.LoggedError() #needs to be create first, other modules need this
import RitRegistration
RitReg = RitRegistration.ritRegistration()

from Config import rooms, BACKUPTIME, BACKUPPATH
from Website import WEB
import LED
import data
from Database import *
import WorkerFunctions as WF



time.sleep(1) #give modules some time to initialize global variables

#--------------------------------------------------------------------


for key in rooms:
    print(key + ' room is created')

#add and start all threads for every light and for the pi
threads = {}
threads['pi'] = threading.Thread(target = WF.PiControl, args = (rooms,))
threads['pi'].daemon = True
threads['pi'].start()

for room in rooms:
    try:
        if "lights" in rooms[room]:
            for key, value in rooms[room]['lights'].items():
                threads[key] = threading.Thread(target = WF.Worker, args = (value,))
                threads[key].daemon = True
                threads[key].start()
                print(room + " " + key + " started a new thread")
                time.sleep(0.5)
    except Exception as E:
        ErrorDB.LogError("Startup Failure", E, "There was a problem while starting up all the threads. (Main:46)", datetime.datetime.now(), False)
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

