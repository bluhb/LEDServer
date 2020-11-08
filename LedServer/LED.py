# all classes for the led strips.
import __main__ as main
import serial
import time
import struct
import sys
import requests as rq

import adafruit_dotstar
import board
from functools import lru_cache
import random
import colorsys

#modules for functions
import math as Math
import time as time

import datetime
from LEDData import SunRise

#------ class for arduino ledstrip, expected at serial port at usb(/dev/ttyUSB0).
#------ in the future a class for wifi enabled led strips will come.

class HSV:
    def __init__(self, ColorCorrection):
        self.H = 0
        self.S = 0
        self.V = 0
        self.ColorCorrection = ColorCorrection
        return None

    def __setattr__(self, Name, Value):
        try:
            if Name in "S,V":
                if 0<= Value <= 100:
                    if Value > 0:
                        Value = Value + self.ColorCorrection[Name]
                        self.__dict__[Name] = self.CheckGreaterThan(Value, 100, "Ceill")
                    else:
                        self.__dict__[Name] = 0
                else:
                    raise ValueError("{} is a too high or low value, must be 0<{}>100".format(Name,Name))
            elif Name in "H":
                if  0 <= Value <= 360:
                    if Value > 0:
                        Value = Value + self.ColorCorrection[Name]
                        self.__dict__[Name] = self.CheckGreaterThan(Value, 360, "Wrap")
                    else:
                        self.__dict__[Name] = 0
                else:
                    raise ValueError("{} is a too high or low value, must be 0<{}>360".format(Name,Name))
            elif Name == "ColorCorrection":
                self.__dict__[Name] = Value
            else:
                raise AttributeError("{} Does not exist in HSV class".format(Name))

        except Exception as e:
            print(e)

    def CheckGreaterThan(self, Value, Check, WrapOrCeill):
        if Value > Check:
            if WrapOrCeill == "Wrap":
                Value = Value - Check
            elif WrapOrCeill == "Ceill":
                Value = Check
        elif Value < 0:
            if WrapOrCeill == "Wrap":
                Value = Value + Check
            elif WrapOrCeill == "Ceill":
                Value = 0
        return Value

    def SetHSV(self, H, S, V):
        self.H = H
        self.S = S
        self.V = V

    def GetHSV(self):
        Color = {"h":self.H, "s":self.S, "v":self.V}
        for key, value in Color.items():
            value = value - self.ColorCorrection[key.upper()]
            Check = 100 if value in ["S", "V"] else 360
            Ceill = "Ceill" if value in ["S", "V"] else "Wrap"
            Color[key] = self.CheckGreaterThan(value, Check, Ceill)
        return Color

    def ToRGB(self):
        return(tuple(round(i*255) for i in colorsys.hsv_to_rgb(self.H/360, self.S/100, self.V/100)))

    def FromRGB(self, RGB):
        Factor = [360, 100, 100]
        RGB = [i/255 for i in RGB]
        hsv = colorsys.rgb_to_hsv(*RGB)
        hsv = tuple(round(i*Factor[x]) for x,i in enumerate(hsv))
        self.H = hsv[0]
        self.S = hsv[1]
        self.V = hsv[2]
        return None


class GenericLed:
    def __init__(self):
        return None

    def __setattr__(self, Name, Value):
        if Name == "function" and getattr(self, "function", None) != "off" and hasattr(self, Name):
            self.oldFunction = self.function
            self.__dict__[Name] = Value
        else:
            self.__dict__[Name] = Value
        return None


    def off(self): #set color to black and set function to colorfill
        V = self.HSV.V
        for i in range(V, 0, -1):
            T = time.perf_counter_ns()
            self.colorfill()
            self.HSV.V = i
            while time.perf_counter_ns() - T < 5000000: #wait for 0.005 second
                pass
        self.HSV.V = 0
        self.colorfill()
        time.sleep(0.01)
        return None

    def on(self):
        self.HSV.V = 100
        self.function = self.oldFunction
        return None

    def colorfade(self): #colorfade the led strip
        for angle in range(0, 360):
            if self.function == "colorfade":
                Prev = time.perf_counter()
                self.HSV.H = angle
                self.HSV.S = 100
                self.colorfill(TimeOut = 0.007)
                while time.perf_counter() - Prev < self.Speed:
                    pass
            else:
                break
        return None

    def sunRise(self, Duration = 1):
        global SunRise
        Steps = len(SunRise["red"])
        for i in range(0,Steps):
            if self.function == "sunrise":
                self.HSV.FromRGB([SunRise["red"][i],
                        SunRise["green"][i],
                        SunRise["blue"][i]
                        ])
                self.colorfill()
                time.sleep((Duration * 60)/Steps)
            else:
                break
        return None

    def sunSet(self, Duration = 5):
        global SunRise
        Steps = len(SunRise["red"])
        for i in range(Steps-1, 0, -1):
            if self.function == "sunset":
                self.HSV.FromRGB([SunRise["red"][i],
                        SunRise["green"][i],
                        SunRise["blue"][i]
                        ])
                self.colorfill()
                time.sleep((Duration * 60)/Steps)
            else:
                break
        return None

    def exit(self):
        return None

#------ class for arduino ledstrip.

class Arduino(GenericLed):
    def __init__(self, name, serialPort, master = None, roomSensors = None, ColorCorrection={"H":0, "S":0, "V":0}): #initialize object
        print(name +" is initializing, after that it will brighten up your day!")
        self.roomSensors = roomSensors
        self.master = master
        self.sync = False #boolean used to sync colorfades with master
        self.device = '/dev/' + str(serialPort)
        self.name = name
        self.arduino = serial.Serial(self.device, 115200)

        self.HSV = HSV(ColorCorrection)
        self.TempHumid = {}
        self.Speed = 0.1
        self.brightness = 1
        self.function = 'off'
        self.oldFunction = "colorfill"
        self.functdict = {
                'colorfill': self.colorfill,
                'on': self.on,
                "off": self.off,
                'colorfade': self.colorfade,
                'sunrise': self.sunRise,
                'sunset': self.sunSet,
                'on': self.on}
        self.prevMilli = time.perf_counter()
        self.now = time.time()
        self.interval = 305

        self.arduino.flushInput()
        self.arduino.flushOutput()
        for i in range(0,4): #schrijf buffer van arduino vol
            self.arduino.write(struct.pack('?', False))
            time.sleep(0.1)
        self.FirstTime = True
        return None

    def main(self): #run the function and check if the sensors need to be read. If sync option is set then sync with master
        self.functdict[self.function]()
        self.now = time.perf_counter_ns()
        if (self.now - self.prevMilli >= self.interval*1000000000) and not (self.roomSensors == None) or self.FirstTime:
            self.Read()
            self.FirstTime = False
            self.prevMilli = time.perf_counter_ns()
        if self.sync and not self.master == None:
            self.Speed = main.rooms[self.master['room']]['lights'][self.master['light']].Speed
            self.HSV = main.rooms[self.master['room']]['lights'][self.master['light']].HSV
            if not self.function == 'colorfill':
                self.function = 'colorfill'
        while time.perf_counter_ns() - self.now < self.Speed*1000000000:
            pass
        return None

    def colorfill(self, TimeOut = 0): #write colors to the arduino
        RGB = self.HSV.ToRGB()
        data = struct.pack('>BBB',
            int(RGB[0]),
            int(RGB[1]),
            int(RGB[2]))
        self.arduino.write(struct.pack('?', True))
        self.arduino.write(data)
        return None

    def Read(self): #read out the serial data from arduino and dump it in the room object
        humidTempB = self.arduino.readline()
        humidTempD = humidTempB.decode()
        humidTemp = humidTempD.rstrip()
        val = humidTemp.split(",")
        t = time.localtime()
        Time = time.strftime("%d-%m-%Y %H:%M:%S", t)
        json = {'time': Time, 'temperature':float(val[0]) - 2, 'humidity':float(val[1]), 'ldr':float(val[2])}
        main.rooms[self.roomSensors]['room'].json.update(json)
        main.rooms[self.roomSensors]['room'].writeToDB()
        print(json)
        time.sleep(0.01)
        return None

    def exit(self):
        self.arduino.close()
        return None


# -------- class for APA102 led strip, expected at the SPI pins of the raspberry pi
class APALedstrip(GenericLed):
    def __init__(self, name, master = None, pixels = 135, ColorCorrection={"H":0, "S":0, "V":0}): #initialize object
        print(name +" is initializing, after that it will brighten up your day!")
        self.master = master
        self.sync = False #boolean used to sync colorfades with master
        self.pixels = adafruit_dotstar.DotStar(
		board.SCK,
		board.MOSI,
		pixels,
		brightness=1,
		auto_write=False)
        self.name = name
        self.brightness = 1
        self.HSV = HSV(ColorCorrection)
        self.Speed = 0.1
        self.length = pixels
        self.now = time.perf_counter_ns()
        self.function = 'off'
        self.oldFunction = "colorfill"
        self.functdict = {
                'colorfill': self.colorfill,
                'on': self.on,
                "off": self.off,
                'colorfade': self.colorfade,
                'sunrise': self.sunRise,
                'sunset': self.sunSet,
                'rainbow': self.rainbow,
                'on':self.on}
        return None

    def main(self): #check for sync, copy colors from dict to array and run the function
        self.now = time.perf_counter_ns()
        if self.sync and not self.master == None:
            self.Speed = main.rooms[self.master['room']]['lights'][self.master['light']].Speed
            self.HSV = main.rooms[self.master['room']]['lights'][self.master['light']].HSV

        self.functdict[self.function]()
        while time.perf_counter_ns() - self.now < self.Speed*1000000000:
            pass
        return None

    def colorfill(self, TimeOut = 0): #fill the whole strip with the same color, every pixel higher than length will be black
        Color = self.HSV.ToRGB()
        self.pixels.fill(Color)
        # for i in range(0,len(self.pixels), 1):
            # if i < int(self.length):
                # self.pixels[i] = tuple(Color)
            # else:
                # self.pixels[i] = (0,0,0)
        self.pixels.show()
        return None

    def rainbow(self): #run a rainbow across the ledstrip, account for set length
        offset = (360)/int(self.length)
        self.HSV.S = 100
        if self.length < 1: self.length = 1
        for angle in range(0,360, 1): #loop from zero to 200 pi, because you can't loop in floats
            if self.function == "rainbow":
                Time = time.perf_counter()
                for j in range(0, len(self.pixels),1):
                    if j < int(self.length):
                        angle = angle + offset #calculate offset with angle, this will make sure every led is another color
                        if angle > 360: angle = angle - 360
                        self.HSV.H = angle
                        Color = self.HSV.ToRGB()
                        self.pixels[j] = tuple(Color)
                    else:
                        self.pixels[j] = (0,0,0)
                self.pixels.show()
                while time.perf_counter() - Time < self.Speed:
                    pass
            else:
                break
        return None

class WiFiLight(GenericLed):
    def __init__(self, Name, IP_ADRESS, Master=None, ColorCorrection={"H":0, "S":0, "V":0}):
        self.Adress = "http://"+IP_ADRESS+"/color"
        self.LastSendTime = None
        self.OldColor = []
        self.Speed = 0.1
        self.HSV = HSV(ColorCorrection)
        self.brightness = 1
        self.now = time.perf_counter_ns()
        self.function = "off"
        self.oldFunction = "colorfill"
        self.master = Master
        self.sync = False
        self.functdict = {"on":self.on,
                "off": self.off,
                "colorfill": self.colorfill,
                "colorfade": self.colorfade,
                "sunrise": self.sunRise}
        try:
            Re = rq.get("http://"+IP_ADRESS)
        except Exception as E:
            print(E)
            print(Name, "Had a connection error")
        self.name = Name

    def colorfill(self, TimeOut = 0.01):
        #print("Check ", "r"+str(color[0])+"g"+str(color[1])+"b"+str(color[2]))

        def padding(x):
            Padding = 3 - len(str(x))
            R = ""
            for _ in range(0, Padding):
                R += "0"
            R += str(x)
            return R
        Color = self.HSV.ToRGB()
        Colors = [padding(x) for x in Color]
        if not self.OldColor == Colors or time.perf_counter() > self.LastSendTime + 60: #don't resend already send colors, unless 1 minute have past. Have to remake wifi light in udp.
            self.OldColor = Colors
            self.LastSendTime = time.perf_counter()
            try:
                Re = rq.post(self.Adress, json = str(Colors[0])+str(Colors[1])+str(Colors[2]), timeout = TimeOut)
                #print("Check ", "r"+str(color[0])+"g"+str(color[1])+"b"+str(color[2]))
            except Exception as E:
                pass

    def main(self):
        self.now = time.perf_counter_ns()
        if self.sync and not self.master == None:
            self.Speed = main.rooms[self.master['room']]['lights'][self.master['light']].Speed
            self.HSV = main.rooms[self.master['room']]['lights'][self.master['light']].HSV
            if not self.function == 'colorfill':
                self.function = 'colorfill'
        self.functdict[self.function]()
        while time.perf_counter_ns() - self.now < self.Speed*1000000000:
            pass
