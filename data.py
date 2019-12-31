# classes for data, at the moment rooms.
from tinydb import TinyDB, Query
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar



class room:
    def __init__(self, name, dataKeys):
        self.Database = name + ".json"
        self.db = TinyDB(self.Database)
        self.sensorData = self.db.table('sensors')
        self.name = name
        self.json = {}
        self.dataKeys = dataKeys
        for value in dataKeys:
            self.json[value] = -1
        return None

    def plot(self, ax, Title, Row, DataX, DataY, MaxRow):
        # plt.subplot(MaxRow, 1, Row)
        # plt.plot(DataX, DataY, linewidth = 0.5)
        # #step = int(len(DataX)/12) if int(len(DataX)/12) > 0 else 1
        # #print("step {}".format(step))
        # #plt.xticks(np.arange(len(DataX), step = step), calendar.month_name[1:13], rotation=20)
        # #plt.format_xdata = mdates.DateFormatter('%B')
        # plt.ylabel(Title)

        ax[Row].plot(DataX, DataY, linewidth=0.5)
        ax[Row].format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax[Row].xaxis.set_tick_params(rotation=10, labelsize=10)
        ax[Row].set_title(Title)
        return None

    def createFig(self):
        plt.clf()
        i = 0
        PlotData = {}
        for value in self.dataKeys:
            PlotData[value] = []

        Time = []
        MaxRow = len(PlotData)

        fig, ax = plt.subplots(MaxRow,1, figsize=(10,5))
        plt.subplots_adjust(hspace = 1)

        for value in self.sensorData.all():
            for key in PlotData:
                PlotData[key].append(float(value['data'][key]))
            Time.append(np.datetime64(value['time']))

        for Key,Value in PlotData.items():
            self.plot(ax, Key, i, Time, Value, MaxRow)
            i += 1

        plt.savefig('./Website/static/'+self.name+'.jpg', dpi=300)
        return None


