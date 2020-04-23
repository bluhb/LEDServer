from datetime import datetime
from Database import *


class ritRegistration():
    def __init__(self):
        self.DB = DataBase("Ritregistratie.sqlite")
        self.Table = "Ritten"
        self.DB.connectOrCreateTable(self.Table,
                    [["KMStand", "INTEGEER"],
                     ["BeginEindPunt", "VARCHAR"],
                     ["Getankt", "INTEGER"],
                     ["Time", "VARCHAR"]],
                    )

    def insertMileage(self, KM, BeginEndPoint, Tanked = 0):
        self.DB.insertToTable2(self.Table,
                    [["KMStand", KM],
                    ["BeginEindPunt", BeginEndPoint],
                    ["Getankt", Tanked],
                    ["Time", datetime.now()]
                    ])
        return True

    def getAllData(self):
        return(self.DB.selectAllDataFromTable(self.Table))
