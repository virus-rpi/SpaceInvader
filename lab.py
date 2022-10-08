import dbManeger

db = dbManeger.dbManeger(r"ip.db")
print(db.execute('SELECT seq FROM sqlite_sequence WHERE name = "ip"')[0][0])