import dbManeger
from mcstatus import JavaServer

db = dbManeger.dbManeger(r"ip.db")
# print(db.execute('SELECT MAX(nr) FROM ip')[0][0])

server = JavaServer("93.30.211.177")
q = server.query()
print(q.raw)