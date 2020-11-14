import __main__ as main
import Database
import Config
import time
from datetime import datetime
class HeatControl:
    def __init__(self, Room, ControllerIP, Wait = 300):
        self.Room = Room
        self.ControllerIP = ControllerIP
        self.Wait = Wait
        self.Keys = Config.TempKeys #Time and Setpoint
        self.Table = Config.TempDBTable + self.Room
        self.DB = Database.DataBase()
        self.DB.connectTable(self.Table, Config.TempDBKeys)
        self.State = "Init"
        return None

    def main(self):
        while True:
            time.sleep(self.wait)
            SetPoint = getSetPoint()
            State = checkTemp(SetPoint)
            if isinstance(State, str):
                setHeater(State)
        return None

    def checkTemp(SetPoint):
        RoomTemp = main.rooms[self.Room].json["temperature"]
        if abs(RoomTemp-SetPoint) > 5:
            if RoomTemp == -1: #init value of roomtemps
                return True
            return None
        if RoomTemp > SetPoint:
            return "Off"
        elif RoomTemp == SetPoint:
            return "Off"
        elif RoomTemp < SetPoint:
            return "On"

    def setHeater(State):
        self.State = State

    def getSetPoint(self):
        CurrTime = datetime.now().strftime("%H:%M:%S")
        SetPoint = self.DB.selectClosestTime(Config.TEMPDBTABLE, CurrTime, Config.TIMEKEY)
        return SetPoint

    def insertSetPoints(self, SetPoints):
        print(SetPoints)
        Values = []
        for Key,Value in SetPoints.items():
            Values.append([Key, float(Value), self.Room])
        self.DB.deleteAllDataFromTable(self.Table)
        self.DB.insertBulk(self.Table, self.Keys, Values)
        return None

    def getAllSetPoints(self):
        def convertTimeDeltaToTime(TimeDelta):
            def padZero(String):
                if len(String) <= 1:
                    String = "0" + String
                if len(String) >= 2:
                    return String
                else:
                    return padZero(String)

            Seconds = TimeDelta.seconds
            Hours = Seconds // 3600
            Minutes = (Seconds // 60) - (Hours * 60)
            Hours = padZero(str(Hours))
            Minutes = padZero(str(Minutes))
            return str(Hours) + ":" + str(Minutes) + ":00"
        Data = self.DB.selectAllDataFromTable(self.Table)
        NewData = []
        for x in Data:
            x["tijd"] = convertTimeDeltaToTime(x["tijd"])
            NewData.append(x)
        return NewData

