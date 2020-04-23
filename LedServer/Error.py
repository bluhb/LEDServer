from Database import *
import datetime
import __main__ as main
from datetime import datetime

class LoggedError():
    def __init__(self, DBName = "Error.sqlite"):
        self.DBName = DBName
        self.DB = DataBase(self.DBName)
        self.Table = "Error"
        self.DB.connectOrCreateTable(self.Table,
                [["id", "INTEGER"], ["Name", "VARCHAR"], ["ErrorMessage", "VARCHAR"], ["Time", "VARCHAR"], ["Error", "VARCHAR"]])

    def LogError(self, ErrorName, ErrorCause, ErrorMessage, ErrorTime, Lethal=False):
        Error = [
                    ["Name", ErrorName],
                    ["Time", ErrorTime],
                    ["Error", ErrorCause],
                    ["ErrorMessage", ErrorMessage]
                ]
        self.DB.insertToTable2(self.Table, Error)
        return 0

if __name__ == "__main__":
    ErrorDatabase = LoggedError()
    try:
        dirk = dirk
    except Exception as E:
        print(E)
        ErrorDatabase.LogError("Test Error", E, "Here is a little message" ,datetime.now(), False)
        pass
    print("Dirk")


