import sqlite3
from datetime import datetime
import threading

print("DataBase Class Should be defined")
class DataBase:
    def __init__(self, DB_Name):
        self.lock = threading.Lock()
        self.DB_Name = DB_Name
        self.DB = sqlite3.connect("./DataBases/" + self.DB_Name, check_same_thread = False)
        self.Curr = self.DB.cursor()

    def connectTable(self, Table):
        A = self.Curr.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(Table)).fetchall()

        SqlCommand = """
        CREATE TABLE {} (
            id INTEGER,
            room VARCHAR,
            ldr FLOAT,
            humidity FLOAT,
            temperature FLOAT,
            time VARCHAR,
            PRIMARY KEY (id));
            """.format(Table)
        self.lock.acquire()
        if not len(A) == 1:
            self.Curr.executescript(SqlCommand)
            self.DB.commit()
            self.lock.release()
            return True
        else:
            self.DB.commit()
            self.lock.release()
            return False

    def connectOrCreateTable(self, Table, ColumnList, PrimaryKey="id"):
        self.lock.acquire()
        A = self.Curr.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(Table)).fetchall()
        if len(A) > 0:
            self.DB.commit()
            self.lock.release()
            return False
        else:
            SqlCommand = "CREATE TABLE {} (".format(Table)
            IdFound = False
            for TableEntry in ColumnList:
                ColumnName = TableEntry[0]
                if ColumnName == PrimaryKey:
                    IdFound = True
                ColumnSort = TableEntry[1]
                SqlCommand = SqlCommand + "{} {}".format(ColumnName, ColumnSort.upper()) + ", "

            if PrimaryKey and IdFound:
                SqlCommand = SqlCommand + "PRIMARY KEY ({}));".format(PrimaryKey)
            else:
                SqlCommand = SqlCommand + "{} INTEGER, PRIMARY KEY ({}));".format(PrimaryKey, PrimaryKey)
            self.Curr.executescript(SqlCommand)
            self.DB.commit()
            self.lock.release()
            return True

    def insertToTable(self, Table, Room, LDR, Humid, Temp, Time):
        SqlCommand = "INSERT INTO {} (room, ldr, humidity, temperature, time) values ({},{},{},{},{})".format(
        "'"+str(Table)+"'", "'"+str(Room)+"'", float(LDR), float(Humid), float(Temp), "'"+str(Time)+"'")

        try:
            self.lock.acquire()
            self.Curr.execute(SqlCommand)
            self.DB.commit()
            self.lock.release()
            return True
        except Exception as E:
            ErrorDB = __main__.ErrorDB
            ErrorDB.LogError("Database Error", E, "Adding to the database went wrong", datetime.now())
            print("Help, this error happenend: {}".format(E))
            return False

    def insertToTable2(self, Table, InsertKeyValues):
        SqlCommand = "INSERT INTO {} (".format(Table)
        for i in range(0,len(InsertKeyValues)):
            Key = InsertKeyValues[i][0]
            SqlCommand = SqlCommand + "{}".format(Key)
            if not i == (len(InsertKeyValues) - 1):
                SqlCommand = SqlCommand + ", "
            else:
                SqlCommand = SqlCommand + ") values ("

        for i in range(0, len(InsertKeyValues)):
            Value = InsertKeyValues[i][1]
            if not i == (len(InsertKeyValues) - 1):
                SqlCommand = SqlCommand + """"{}", """.format(Value)
            else:
                SqlCommand = SqlCommand + """"{}")""".format(Value)
        print(SqlCommand)
        self.lock.acquire()
        self.Curr.execute(SqlCommand)
        self.DB.commit()
        self.lock.release()
        return None



    def selectAllSensorsByRoom(self, Room, Table, LastNItems = 600, PrimaryKey = "id"):
        SqlCommand = """SELECT * FROM {} WHERE room="{}" and id > (select MAX({}) - {} FROM {}) """.format(Table, Room, PrimaryKey, int(LastNItems), Table)
        print(SqlCommand)
        self.lock.acquire()
        DataRaw = self.Curr.execute(SqlCommand)
        self.lock.release()
        KeysRaw = DataRaw.description
        DataLists = DataRaw.fetchall()
        Keys = [KeyList[0] for KeyList in KeysRaw]
        Data = []
        for DataSet in DataLists:
            DataDict = {}
            for i in range(0, len(Keys)):
                DataDict[Keys[i]] = DataSet[i]
            Data.append(DataDict)
        return Data

    def selectAllDataFromTable(self, Table, LastNItems = 500, PrimaryKey = "id"):
        SqlCommand = """SELECT * FROM {} WHERE id > (select MAX({}) - {} FROM {})""".format(
                Table,
                PrimaryKey,
                LastNItems,
                Table)
        self.lock.acquire()
        DataRaw = self.Curr.execute(SqlCommand)
        self.lock.release()
        KeysRaw = DataRaw.description
        DataLists = DataRaw.fetchall()
        Keys = [KeyList[0] for KeyList in KeysRaw]
        Data = []
        for DataSet in DataLists:
            DataDict = {}
            for i in range(0, len(Keys)):
                DataDict[Keys[i]] = DataSet[i]
            Data.append(DataDict)
        return Data

    def closeDB(self):
        self.DB.commit()
        self.DB.close()
        return None

if __name__ == "__main__":
    DB = DataBase("Test")
    DB.connectOrCreateTable("Test", [["Dirk", "integer"], ["room", "string"]])
    DB.insertToTable2("Test", [["Dirk", 1], ["room", "Bluhb"]])
    DB2 = DataBase("Test")
    DB2.connectOrCreateTable("Test", [])
    Data2 = DB2.selectAllSensorsByRoom("Bluhb", "Test")
    print(Data2)
    Data = DB.selectAllSensorsByRoom("Bluhb", "Test")
    print(Data)

