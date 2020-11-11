# classes for data, at the moment rooms.
from datetime import datetime
import numpy as np
import calendar
from Database import *


class room:
    def __init__(self, name, dataKeys):
        self.DB = DataBase()
        self.Table = "Sensor"
        self.DB.connectTable(self.Table, dataKeys)
        self.name = name
        self.json = {}
        self.dataKeys = dataKeys
        for value in dataKeys:
            self.json[value[0]] = -1
        self.json["room"] = self.name
        return None

    # def plot(self, ax, Title, Row, DataX, DataY, MaxRow):
        # # plt.subplot(MaxRow, 1, Row)
        # # plt.plot(DataX, DataY, linewidth = 0.5)
        # # #step = int(len(DataX)/12) if int(len(DataX)/12) > 0 else 1
        # # #print("step {}".format(step))
        # # #plt.xticks(np.arange(len(DataX), step = step), calendar.month_name[1:13], rotation=20)
        # # #plt.format_xdata = mdates.DateFormatter('%B')
        # # plt.ylabel(Title)
        # if not (len(DataX) < 30):
            # Ticks = [DataX[i] for i in range(0,len(DataX), 25)]
            # Ticks.append(DataX[-1])
        # else:
            # Ticks = DataX
        # ax[Row].plot(DataX, DataY, linewidth=0.5)
        # #ax[Row].format_xdata = mdates.DateFormatter('%Y-%m-%d')
        # ax[Row].xaxis.set_tick_params(rotation=25, labelsize=7)
        # ax[Row].set_xticks(Ticks)
        # ax[Row].set_title(Title)
        # return None

    # def createFig(self):
        # try:
            # plt.clf()
            # i = 0
            # PlotData = {}
            # for value in self.dataKeys:
                # PlotData[value] = []

            # Time = []
            # MaxRow = len(PlotData)

            # fig, ax = plt.subplots(MaxRow,1, figsize=(10,7))
            # plt.subplots_adjust(hspace = 1)

            # for value in self.DB.selectAllSensorsByRoom(self.name, self.Table, LastNItems = 600, PrimaryKey = "id"):
                # for key in PlotData:
                    # PlotData[key].append(float(value[key]))
                # Time.append(value['time'])

            # for Key,Value in PlotData.items():
                # self.plot(ax, Key, i, Time, Value, MaxRow)
                # i += 1

            # plt.savefig('./Website/static/'+self.name+'.jpg', dpi=300)
            # plt.close()
            # del PlotData, Time
            # return None
        # except Exception as E:
            # ErrorDB.LogError("GraphError",
                    # E,
                    # "Something went wrong while creating the graphs",
                    # datetime.now(),
                    # False)
            # pass

    def writeToDB(self):
        Data = []
        for key, value in self.json.items():
            Data.append([key, value])
        # self.DB.insertToTable(self.Table, self.name, LDR, Humid, Temp, Time)
        print("writeToDB: {}".format(Data))
        self.DB.insertToTable2(self.Table, Data)
        self.DB.DB.commit()
        return None

    def getDataFromDB(self, Items = 600):
        DataRaw = self.DB.selectAllSensorsByRoom(self.name, self.Table, Items)
        Data = {}
        Time = []
        print("getDataFromDB: name; {}, table; {}".format(self.name, self.Table))
        for value in self.dataKeys:
            if not (value[0] == "room"):
                Data[value[0]] = []

        for value in DataRaw:
            for key in Data:
                try:
                    Data[key].append(float(value[key]))
                except:
                    Data[key].append(value[key])
        print(Data.keys())
        return Data
