import sqlite3
db = sqlite3.connect("./Ritregistratie.sqlite")
Curr = db.cursor()

Command = "DELETE FROM Ritten WHERE ID=19"
Curr.execute(Command)
db.commit()
