import mysql.connector
from datetime import datetime
import threading
import __main__ as main
import Config

"""
This module handles all database connections.
It practically is a wrapper and expansion on the standard SQLITE3 package.

The DB supports multi threaded applications. But insertion will block the threading.
This means no more than 1 insertion to a single database will happen at the same moment.
"""

print("DataBase Class Should be defined")
class DataBase:
    def __init__(self):
        self.lock = threading.Lock()
        self.DB = mysql.connector.connect(
                host="localhost",
                user=Config.DBUser,
                password=Config.DBPassword,
                database=Config.DB
                )
        self.Curr = self.DB.cursor(buffered=True)
        self.Curr.execute("USE ledserver;")
        return None

    def connectTable(self, Table, KeysSort):
        """Table = TableName
        KeysSort is list containing list with key and sort: [["Example", "VARCHAR"], ["Ex", "INTEGER"]]
        """
        self.lock.acquire()
        SqlCommand = "CREATE TABLE IF NOT EXISTS {} ( id INTEGER AUTO_INCREMENT, ".format(Table)
        for KeySort in KeysSort:
            Key = KeySort[0]
            Sort = KeySort[1]
            SqlCommand += Key + " " + Sort + ", "

        SqlCommand += "PRIMARY KEY(id));"
        print(SqlCommand)
        # if not len(A) == 1:
        self.Curr.execute(SqlCommand)
        self.DB.commit()
        self.lock.release()
        return True
        # else:
            # self.DB.commit()
            # self.lock.release()
            # return False

    def insertToTable(self, Table, InsertKeyValues):
        """Insert key:value pairs into the selected table from the DB"""
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
        self.lock.acquire()
        self.Curr.execute(SqlCommand)
        self.DB.commit()
        self.lock.release()
        return None

    def selectAllDataFromTable(self, Table, LastNItems = 500, PrimaryKey = "id", Sort = "id"):
        """select all the data from the given table"""
        SqlCommand = """SELECT * FROM {} WHERE {} > (select MAX({}) - {} FROM {}) ORDER BY {} ASC""".format(
                Table,
                PrimaryKey,
                PrimaryKey,
                LastNItems,
                Table,
                Sort)
        self.lock.acquire()
        self.Curr.execute(SqlCommand)
        DataRaw = self.Curr.fetchall()
        self.lock.release()
        if len(DataRaw) == 0:
            return []
        GetKeysSQL = "SHOW columns FROM {}".format(Table)
        self.Curr.execute(GetKeysSQL)
        Keys = [x[0] for x in self.Curr.fetchall()]
        DataLists = DataRaw
        Data = []
        for DataSet in DataLists:
            DataDict = {}
            for i in range(0, len(Keys)):
                DataDict[Keys[i]] = DataSet[i]
            Data.append(DataDict)
        return Data

    def deleteAllDataFromTable(self, Table):
        SQL = "TRUNCATE TABLE {};".format(Table)
        self.lock.acquire()
        self.Curr.execute(SQL)
        self.DB.commit()
        self.lock.release()
        return None

    def deleteByID(self, ID, Table):
        SQL = "DELETE FROM {} WHERE ID={}".format(Table, ID)
        self.lock.acquire()
        self.Curr.execute(SQL)
        self.DB.commit()
        self.lock.release()
        return None

    def updateById(self, Table, ID, KeyValuePairUpdate):
        SQL = "UPDATE {} SET {}='{}' WHERE ID={}".format(
                Table, KeyValuePairUpdate[0], KeyValuePairUpdate[1], ID)
        self.lock.acquire()
        self.Curr.execute(SQL)
        self.DB.commit()
        self.lock.release()
        return None

    def updateBulkById(self, Table, KeyValueDictList):
        """
        Same as update by id but will handle multiple rows and multiple columns for every row
        """
        SQL = []
        self.lock.acquire()
        for _,Dict in KeyValueDictList.items():
            SQLS = ""
            I = 0
            ID = Dict.pop("id")
            SQLS += "UPDATE {} SET ".format(Table)
            for Key,Value in Dict.items():
                SQLS += "{}='{}'".format(Key, Value)
                if not I == len(Dict) - 1:
                    SQLS += ", "
                else:
                    SQLS += " "
                I += 1
            SQLS += "WHERE ID={};".format(ID)
            self.Curr.execute(SQLS)
        self.DB.commit()
        self.lock.release()
        return None



    def updateByKey(self, Table, KeyValuePairUpdate, KeyValueMatch):
        SQL = """UPDATE {} SET "{}"="{}" WHERE "{}"="{}"; """.format(
                Table, KeyValuePairUpdate[0], KeyValuePairUpdate[1], KeyValueMatch[0], KeyValueMatch[1])
        try:
            self.lock.acquire()
            self.Curr.execute(SQL)
            self.DB.commit()
            self.lock.release()
        except Exception as E:
            print(E)
            return "Error"
        return None

    def selectById(self, Table, ID):
        """Select the data from the table by the id column"""
        SQL = """SELECT * FROM {} WHERE ID={}""".format(Table, ID)
        self.lock.acquire()
        self.Curr.execute(SQL)
        DataLists = self.Curr.fetchall()
        self.lock.release()

        GetKeysSQL = "SHOW columns FROM {}".format(Table)
        self.Curr.execute(GetKeysSQL)
        Keys = [x[0] for x in self.Curr.fetchall()]

        DataDict = {}
        DataSet = DataLists[0]
        for i in range(0, len(Keys)):
            DataDict[Keys[i]] = DataSet[i]
        return DataDict

    def selectCountWhere(self, Table, Where):
        SQL = """SELECT COUNT(*) FROM {} WHERE {};""".format(
                Table,
                Where)
        self.lock.acquire()
        self.Curr.execute(SQL)
        DataLists = self.Curr.fetchall()
        self.lock.release()
        return DataLists

    def selectWhere(self, Table, Where, Sort="id"):
        SQL = """SELECT * FROM {} WHERE {} ORDER BY {} DESC;""".format(
                Table,
                Where,
                Sort)
        self.lock.acquire()
        self.Curr.execute(SQL)
        DataLists = self.Curr.fetchall()
        self.lock.release()
        GetKeysSQL = "SHOW columns FROM {}".format(Table)
        self.Curr.execute(GetKeysSQL)
        Keys = [x[0] for x in self.Curr.fetchall()]

        Data = []
        for DataSet in DataLists:
            DataDict = {}
            for i in range(0, len(Keys)):
                DataDict[Keys[i]] = DataSet[i]
            Data.append(DataDict)
        return Data

    def selectClosestTime(self, Table, Time, TimeKey, Limit=1):
        SQL = """SELECT * FROM {} ORDER BY ABS(TIMEDIFF({}, {})) ASC LIMIT {}""".format(Table, Time, TimeKey, Limit)
        self.lock.acquire()
        self.Curr.execute(SQL)
        DataLists = self.Curr.fetchall()
        self.lock.release()
        GetKeysSQL = "SHOW columns FROM {}".format(Table)
        self.Curr.execute(GetKeysSQL)
        Keys = [x[0] for x in self.Curr.fetchall()]

        Data = []
        for DataSet in DataLists:
            DataDict = {}
            for i in range(0, len(Keys)):
                DataDict[Keys[i]] = DataSet[i]
            Data.append(DataDict)
        return Data

    def formatKeysValues(self, FormatList):
        S = ""
        if isinstance(FormatList[0], str):
            S += "("
            for X in FormatList:
                S += '{}, '.format(X)
            S = S[0:len(S) - 2]
            S += ")"
        elif isinstance(FormatList[0], list):
            for X in FormatList:
                S += "("
                for Y in X:
                    S += '"{}", '.format(Y)
                S = S[0:len(S) - 2]
                S += "), "
            S = S[0:len(S) - 2]
        return S

    def insertBulk(self, Table, Keys, ValueListList):
        SQL = """INSERT INTO {} {} VALUES {};""".format(Table, self.formatKeysValues(Keys), self.formatKeysValues(ValueListList))
        print(SQL)
        self.lock.acquire()
        self.Curr.execute(SQL)
        self.DB.commit()
        self.lock.release()
        return SQL

