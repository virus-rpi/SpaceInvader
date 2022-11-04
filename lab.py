import dbManeger
from mcstatus import JavaServer

db = dbManeger.dbManeger(r"ip.db")
# print(db.execute('SELECT MAX(nr) FROM ip')[0][0])

server = JavaServer("93.30.211.177")
q = server.query()
print(q.raw)

import asyncio

from minecraft import Server

async def main():
    ip = "176.9.20.205"
    port = 25565 # rcon port
    password = ""

    # can be used in a context manager
    async with Server(ip, port, password) as server:
        print(await server.send("list"))

    # can also be used procedurally
    server = Server(ip, port, password, connect_on_send=True)
    # connect_on_send make it so the Server tried to reconnect if
    # it's disconnected, otherwise it raises a NotConnectedError
    print(await server.send("list"))

    for i in await server.online():
        print(f"{i} is online")

    await server.close()

asyncio.run(main())