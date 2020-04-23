from datetime import datetime as dTime
import simpleaudio
import datetime
import time
import threading
import __main__ as main

AlarmDict = {}
AlarmAudioFile = 'sample.wav'

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
        "blue":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
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
                252, 253, 255, 255]
        }




class Alarm:
    def __init__(self, Hour, Minutes, Name, RoomName, PreWakeUp=30):
        self.Hour = int(Hour)
        self.Minutes = int(Minutes)
        self.PreWakeUp = int(PreWakeUp)
        if (self.Minutes - self.PreWakeUp) < 0:
            self.Hour = self.Hour - 1
            self.Minutes = 60 - abs(self.Minutes - self.PreWakeUp)
        else:
            self.Hour = self.Hour
            self.Minutes = self.Minutes - self.PreWakeUp
        self.MinuteRange = 1
        self.MinuteRangeCorrection = 1.1
        self.AlarmOn = True
        self.RoomName = RoomName
        self.TimeString = Hour + ":" + Minutes
        self.Name = Name if not isinstance(Name, (bool,)) else self.TimeString
        # End of setting variables
        #
        print(self.Name + " :Alarm set for: " + str(self.Hour) + " hour " + str(self.Minutes) + " Minute")
        self.applyMinuteRangeCorrection()
        return None

    def applyMinuteRangeCorrection(self):
        self.MinuteRange = self.MinuteRange * self.MinuteRangeCorrection
        return None

    def alarmOn(self):
        global AlarmDict

        while self.AlarmOn and not AlarmDict[self.Name]["Stop"]:
            Now = dTime.now()
            if self.Hour == Now.hour:
                MinuteDiff = self.Minutes - Now.minute
                if MinuteDiff < self.MinuteRange:
                    self.alarmTimeReached()
                    break
                else:
                    time.sleep(1)
            else:
                time.sleep(60)
        AlarmDict.pop(self.Name, False)
        return None

    def alarmTimeReached(self):
        global AlarmDict, SunRise, AlarmAudioFile
        Lights = main.rooms[self.RoomName]['lights']
        Steps = len(SunRise["red"])
        WaveObj = simpleaudio.WaveObject.from_wave_file(AlarmAudioFile)
        PlayObj = WaveObj.play()
        for Light in Lights.values():
            Light.brightness = 1
            Light.wait = (self.PreWakeUp * 60) / Steps
        for i in range(0,Steps):
            if not AlarmDict[self.Name]["Stop"]:
                for Light in Lights.values():
                    Light.color_rgb = {"r": SunRise["red"][i], "g": SunRise["green"][i],"b": SunRise["blue"][i]}
                    time.sleep(int((self.PreWakeUp * 60) / Steps))
            else:
                break
        PlayObj.stop()
        for Light in Lights.values():
            Light.wait = 0.1
        AlarmDict.pop(self.Name, False)
        return None


#----------------------------------------------------------
def handleInput():
    Name = input("AlarmLabel")
    HH = input("Enter HH")
    MM = input("Enter MM")
    if len(Name) == 0:
        Name = False
    return Name, HH, MM

def setupAlarm(HH, MM, Name = False, RoomName = 'livingroom', PreWakeUp = None):
    global AlarmDict
    TimeString = str(HH) + ":" + str(MM)
    Name = Name if not isinstance(Name, (bool,)) else TimeString
    PreWakeUp = int(PreWakeUp) if not PreWakeUp == None else 30

    SetAlarm = Alarm(HH, MM, Name, RoomName, PreWakeUp)
    AlarmDict[Name] = {}
    AlarmDict[Name]["Stop"] = False
    AlarmDict[Name]["Thread"] = threading.Thread(target = SetAlarm.alarmOn)
    AlarmDict[Name]["Thread"].daemon = True
    AlarmDict[Name]["Thread"].start()
    return None

def testAlarm(data):
    print("Alarm.testAlarm: " + data)

if __name__ == "__main__":
    while True:
        Name, HH, MM = handleInput()
        setupAlarm(HH, MM, Name)
        print(AlarmDict)

