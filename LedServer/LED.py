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

import datetime

#------ class for arduino ledstrip, expected at serial port at usb(/dev/ttyUSB0).
#------ in the future a class for wifi enabled led strips will come.

# Thanks to: https://github.com/brendan-ward/sunrise/blob/master/circuitpython/onboard_led.py
SunRise = {
        "red":[15, 17, 26, 35, 43, 52, 61, 70, 79, 87, 96, 105, 114, 123, 131, 140,
               149, 158, 167, 175, 184, 193, 202, 211, 219, 228, 237, 246, 255, 255,
               255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
               255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
               255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
               255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
               255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 254,
               253, 253, 252, 252, 251, 250, 250, 249, 249, 248, 247, 247, 246, 246,
               245, 245, 244, 243, 243, 242, 242, 241, 240, 240, 239, 239, 238, 237,
               237, 236, 236, 235, 235, 234, 233, 233, 232, 232, 231, 230, 230, 229,
               229, 228, 228, 227, 226, 226, 225, 225, 224, 223, 223, 222, 222, 221,
               220, 220, 219, 219, 218, 218, 217, 216, 216, 215, 215, 214, 213, 213,
               212, 212, 211, 211, 210, 209, 209, 208, 208, 207, 206, 206, 205, 205,
               204, 203, 203, 202, 202, 201, 201, 200, 199, 199, 198, 198, 197, 196,
               196, 195, 195, 194, 193, 193, 192, 192, 191, 191, 190, 189, 189, 188,
               188, 187, 186, 186, 185, 185, 184, 184, 183, 182, 182, 181, 181, 180,
               179, 179, 178, 178, 177, 176, 176, 175, 175, 174, 174, 173, 172, 172,
               171, 171, 170, 169, 169, 168, 168, 167, 167, 166, 165, 165, 164, 164,
               163, 162, 162, 161, 161, 160, 159, 159, 158, 158, 157, 157, 156, 155,
               155, 154, 154, 153, 152, 152, 151, 151, 150, 130, 149, 148, 147, 146,
               145, 144, 142, 141, 140, 139, 138, 137, 136, 135, 134, 133, 132, 131,
               130, 129, 128, 127],
        "green":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 6, 8, 10, 13, 15, 17, 19, 21, 23, 26,
                 28, 30, 32, 34, 36, 39, 41, 43, 45, 47, 49, 52, 54, 56, 58, 60, 62,
                 65, 67, 69, 71, 73, 75, 78, 80, 82, 84, 86, 88, 91, 93, 95, 97, 99,
                 101, 104, 106, 108, 110, 112, 114, 117, 119, 121, 123, 125, 128, 128,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
                 130, 130, 130, 130, 130, 130, 129, 128, 127, 126, 125, 124, 122, 121,
                 120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107],
        "blue":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20,
                22, 23, 24, 25, 27, 28, 29, 31, 32, 33, 34, 36, 37, 38, 40, 41, 42, 44,
                45, 46, 47, 49, 50, 51, 53, 54, 55, 57, 58, 59, 60, 62, 63, 64, 66, 67,
                68, 69, 71, 72, 73, 75, 76, 77, 79, 80, 81, 82, 84, 85, 86, 88, 89, 90,
                92, 93, 94, 95, 97, 98, 99, 101, 102, 103, 104, 106, 107, 108, 110,
                111, 112, 114, 115, 116, 117, 119, 120, 121, 123, 124, 125, 127, 128,
                129, 130, 132, 133, 134, 136, 137, 138, 139, 141, 142, 143, 145, 146,
                147, 149, 150, 151, 152, 154, 155, 156, 158, 159, 160, 162, 163, 164,
                165, 167, 168, 169, 171, 172, 173, 174, 176, 177, 178, 180, 181, 182,
                184, 185, 186, 187, 189, 190, 191, 193, 194, 195, 197, 198, 199, 200,
                202, 203, 204, 206, 207, 208, 209, 211, 212, 213, 215, 216, 217, 219,
                220, 221, 222, 224, 225, 226, 228, 229, 230, 232, 233, 234, 235, 236,
                237, 238, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251,
                252, 253, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
        }
class GenericLed:
    def __init__(self):
        return None

    def clear(self): #set color to black and set function to colorfill
        OldBrightness = self.brightness
        for i in range(int(Math.pi*50), 0, -1):
            self.brightness = Math.sin(i/100)
            self.colorfill()
            time.sleep(1/50)
        self.color_rgb = {'r':0, 'g':0, 'b':0}
        self.brightness = OldBrightness
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
            if self.function == "colorfade":
                angle = angle/100
                self.definecolor(angle)
                self.colorfill()
                time.sleep(self.wait)
            else:
                break
        return None

    def sunRise(self, Duration = 5):
        global SunRise
        Steps = len(SunRise["red"])
        for i in range(0,Steps):
            if self.function == "sunrise":
                self.color_rgb = {"r":SunRise["red"][i],
                        "g":SunRise["green"][i],
                        "b":SunRise["blue"][i]
                        }
                self.colorfill()
                print(self.color_rgb)
                time.sleep((Duration * 60)/Steps)
            else:
                break
        return None

    def sunSet(self, Duration = 5):
        global SunRise
        Steps = len(SunRise["red"])
        for i in range(Steps-1, 0, -1):
            if self.function == "sunset":
                self.color_rgb = {"r":SunRise["red"][i],
                        "g":SunRise["green"][i],
                        "b":SunRise["blue"][i]
                        }
                self.colorfill()
                print(self.color_rgb)
                time.sleep((Duration * 60)/Steps)
            else:
                break
        return None

    def exit(self):
        return None

#------ class for arduino ledstrip.
#------ in the future a class for wifi enabled led strips will come.

class Arduino(GenericLed):
    def __init__(self, name, serialPort, master = None, roomSensors = None): #initialize object
        print(name +" is initializing, after that it will brighten up your day!")
        self.roomSensors = roomSensors
        self.master = master
        self.sync = False #boolean used to sync colorfades with master
        self.device = '/dev/' + str(serialPort)
        self.name = name
        self.arduino = serial.Serial(self.device, 115200)
        self.color_rgb = {'r':0, 'g':0, 'b':0}
        self.color = [0,0,0]
        self.TempHumid = {}
        self.wait = 0.1
        self.brightness = 1
        self.function = 'colorfill'
        self.functdict = {'colorfill': self.colorfill,
                'colorfade': self.colorfade,
                'sunrise': self.sunRise,
                'sunset': self.sunSet,
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
        humidTempB = self.arduino.readline()
        humidTempD = humidTempB.decode()
        humidTemp = humidTempD.rstrip()
        val = humidTemp.split(",")
        t = time.localtime()
        Time = time.strftime("%d-%m-%Y %H:%M:%S", t)
        json = {'time': Time, 'temperature':val[0], 'humidity':val[1], 'ldr':val[2]}
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
    def __init__(self, name, master = None, pixels = 135): #initialize object
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
        self.color_rgb = {'r':0,'g':0,'b':0}
        self.color = [0,0,0]
        self.brightness = 1
        self.wait = 0.1
        self.length = pixels
        self.function = 'colorfill'
        self.functdict = {'colorfill': self.colorfill,
                'colorfade': self.colorfade,
                'sunrise': self.sunRise,
                'sunset': self.sunSet,
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
        color = [int(self.color_rgb["r"] * self.brightness), int(self.color_rgb["g"] * self.brightness),
                int(self.color_rgb["b"] * self.brightness)]

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
            if self.function == "rainbow":
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
            else:
                break
        return None
