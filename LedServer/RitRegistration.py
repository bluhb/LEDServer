from datetime import datetime
from Database import *


class ritRegistration():
    def __init__(self):
        self.DB = DataBase()
        self.Table = "Ritten"
        self.DB.connectTable(self.Table,
                    [["KMStand", "INTEGEER"],
                     ["BeginEindPunt", "VARCHAR[500]"],
                     ["Getankt", "INTEGER[500]"],
                     ["Time", "DATE"]],
                    )

    def insertMileage(self, KM, BeginEndPoint, Tanked = 0):
        self.DB.insertToTable2(self.Table,
                    [["KMStand", KM],
                    ["BeginEindPunt", BeginEndPoint],
                    ["Getankt", Tanked],
                    ["Time", str(datetime.now())]
                    ])
        return True

    def getAllData(self):
        return(self.DB.selectAllDataFromTable(self.Table))

    def averageMileage(self):
        DataRaw = self.DB.selectAllDataFromTable(self.Table)
        DataTank = []
        AVGs = []
        for X in DataRaw:
            if X["Getankt"] > 0:
                DataTank.append(X)
        for i in range(0, len(DataTank)-1, 1):
            KM = DataTank[i+1]["KMStand"] - DataTank[i]["KMStand"]
            Liters = DataTank[i+1]["Getankt"]
            AVGs.append(KM/Liters)
        return AVGs, sum(AVGs)/len(AVGs)
