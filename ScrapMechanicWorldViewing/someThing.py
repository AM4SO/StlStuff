import sqlite3
import json

dbPath = "16 bit computer.db"
if True:
    dbPath = input("world db file: ")

con = sqlite3.connect(dbPath)
cur = con.cursor()
done = False
first = True

print("Printing database tables...")
print("SELECT * FROM sqlite_master WHERE type='table'")
while not done:
    if not first:
        x=input("command: ")
    else:
        x="SELECT * FROM sqlite_master WHERE type='table'"
        first = False
    done = x=="exit"
    if not done:
        try:
            res = cur.execute(x)
            if res:
                y = res.fetchall()
                [print(v) for v in y]#print(json.dumps(y, indent=4))
        except sqlite3.OperationalError as e:
            print(e)


con.close()
