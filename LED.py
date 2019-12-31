# all classes for the led strips.
import __main__ as main
import serial
import time
import struct
import sys

import adafruit_dotstar
import board
from functools import lru_cache
import random

#modules for functions
import math as Math
import time as time

from tinydb import TinyDB, Query
import datetime

#------ class for arduino ledstrip, expected at serial port at usb(/dev/ttyUSB0).
#------ in the future a class for wifi enabled led strips will come.

db = TinyDB('Database.json')
sensorData = db.table('sensors')

class GenericLed:
    def __init__(self):
        return None

    def clear(self): #set color to black and set function to colorfill
        self.color_rgb = {'r':0, 'g':0, 'b':0}
        self.function = 'colorfill'
        return None

    def definecolor(self, angle): #calculate the color for the colorfade
        pi = Math.pi
        self.color[0] = int(Math.sin(angle)*127+128)
        self.color[1] = int(Math.sin(angle + 0.66*pi)*127+128)
        self.color[2] = int(Math.sin(angle + 1.33*pi)*127+128)
        self.color_rgb['r'] = self.color[0]
        self.color_rgb['g'] = self.color[1]
        self.color_rgb['b'] = self.color[2]
        return None

    def colorfade(self): #colorfade the led strip
        pi = Math.pi
        for angle in range(0, int(200*pi), 1):
            angle = angle/100
            self.definecolor(angle)
            self.colorfill()
            time.sleep(self.wait)
        return None

    def exit(self):
        return None

#------ class for arduino ledstrip.
#------ in the future a class for wifi enabled led strips will come.

class Arduino(GenericLed):
    def __init__(self, name, serialPort, room, master = None, roomSensors = None): #initialize object
        global sensorData
        self.room = room
        self.roomSensors = roomSensors
        self.master = master
        self.sync = False #boolean used to sync colorfades with master
        self.device = '/dev/' + str(serialPort)
        self.name = name
        self.arduino = serial.Serial(self.device, 115200)
        self.color_rgb = {'r':0, 'g':0, 'b':0}
        self.color = [0,0,0]
        self.sensorData = sensorData
        self.TempHumid = {}
        self.wait = 0.1
        self.brightness = 1
        self.function = 'colorfill'
        self.functdict = {'colorfill': self.colorfill,
                'colorfade': self.colorfade,
                'clear': self.clear}
        self.prevMilli = time.perf_counter()
        self.now = time.time()
        self.interval = 305

        self.arduino.flushInput()
        self.arduino.flushOutput()
        for i in range(0,4): #schrijf buffer van arduino vol
            self.arduino.write(struct.pack('?', False))
            time.sleep(0.1)
        return None

    def main(self): #run the function and check if the sensors need to be read. If sync option is set then sync with master
        self.functdict[self.function]()
        self.now = time.perf_counter()
        if (self.now - self.prevMilli >= self.interval) and not (self.roomSensors == None):
            self.Read()
            self.prevMilli = time.perf_counter()
        if self.sync and not self.master == None:
            self.wait = main.rooms[self.master['room']]['lights'][self.master['light']].wait
            self.color_rgb = main.rooms[self.master['room']]['lights'][self.master['light']].color_rgb
            self.brightness = main.rooms[self.master['room']]['lights'][self.master['light']].brightness
            if not self.function == 'colorfill':
                self.function = 'colorfill'
        return None

    def colorfill(self): #write colors to the arduino
        data = struct.pack('>BBB',
            int(self.color_rgb['r']*self.brightness),
            int(self.color_rgb['g']*self.brightness),
            int(self.color_rgb['b']*self.brightness))
        self.arduino.write(struct.pack('?', True))
        self.arduino.write(data)
        return None

    def Read(self): #read out the serial data from arduino and dump it in the room object
        try:
            humidTempB = self.arduino.readline()
            humidTempD = humidTempB.decode()
            humidTemp = humidTempD.rstrip()
            val = humidTemp.split(",")
            json = {'temp':val[0], 'humid':val[1], 'LDR':val[2]}
            main.rooms[self.roomSensors]['room'].json = json
            main.rooms[self.roomSensors]['room'].sensorData.insert(
                    {'time':str(datetime.datetime.now()), 'data':json})
            self.sensorData.insert({'time':str(datetime.datetime.now()),'data':json})
            print(json)
            time.sleep(0.01)
        except:
            pass
        return None

    def exit(self):
        self.arduino.close()
        return None


# -------- class for APA102 led strip, expected at the SPI pins of the raspberry pi
class APALedstrip(GenericLed):
    def __init__(self, name, room, master = None, pixels = 135): #initialize object
        self.room = room
        self.master = master
        self.sync = False #boolean used to sync colorfades with master
        self.pixels = adafruit_dotstar.DotStar(
		board.SCK,
		board.MOSI,
		pixels,
		brightness=1,
		auto_write=False)
        self.name = name
        self.color_rgb = {'r':0,'g':0,'b':0}
        self.color = [0,0,0]
        self.brightness = 1
        self.wait = 0.1
        self.length = pixels
        self.function = 'colorfill'
        self.functdict = {'colorfill': self.colorfill,
                'colorfade': self.colorfade,
                'rainbow': self.rainbow,
                'clear':self.clear}
        return None

    def main(self): #check for sync, copy colors from dict to array and run the function
        if self.sync and not self.master == None:
            self.wait = main.rooms[self.master['room']]['lights'][self.master['light']].wait
            self.color_rgb = main.rooms[self.master['room']]['lights'][self.master['light']].color_rgb
            self.brightness = main.rooms[self.master['room']]['lights'][self.master['light']].brightness

        self.color[0] = self.color_rgb['r']
        self.color[1] = self.color_rgb['g']
        self.color[2] = self.color_rgb['b']
        self.functdict[self.function]()
        return None

    def colorfill(self): #fill the whole strip with the same color, every pixel higher than length will be black
        color = [int(i*self.brightness) for i in self.color]

        for i in range(0,len(self.pixels), 1):
            if i < int(self.length):
                self.pixels[i] = tuple(color)
            else:
                self.pixels[i] = (0,0,0)
        self.pixels.show()
        return None

    def rainbow(self): #run a rainbow across the ledstrip, account for set length
        pi = Math.pi
        offset = (2*pi)/int(self.length)
        if self.length < 1: self.length = 1
        for angle in range(0,int(200*pi), 5): #loop from zero to 200 pi, because you can't loop in floats
            angle = angle/100
            for j in range(0, len(self.pixels),1):
                if j < int(self.length):
                    angle = angle + offset #calculate offset with angle, this will make sure every led is another color
                    self.definecolor(angle)
                    color = [int(i*self.brightness) for i in self.color]
                    self.pixels[j] = tuple(color)
                else:
                    self.pixels[j] = (0,0,0)
            self.pixels.show()
            time.sleep(self.wait)
        return None
