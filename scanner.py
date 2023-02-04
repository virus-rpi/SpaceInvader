import dbManeger
from mcstatus import JavaServer
import time
import requests
import json
import socket
from progress.bar import Bar
def read(sock, n):
    o = b""
    while len(o) < n:
        o += sock.recv(n - len(o))
    return o


# Read a varint from the socket
def read_varint(sock, remaining=0):
    o = 0
    for i in range(5):
        b = ord(sock.recv(1))
        o |= (b & 0x7F) << 7 * i
        if not b & 0x80:
            return remaining - (i + 1), o


# Read a packet header from the socket
def read_header(sock, compression=False):
    # Packet length
    _, length = read_varint(sock)

    # Compression (1.8+, only if enabled)
    if compression:
        length, _ = read_varint(sock, length)

    # Packet ident
    length, packet_ident = read_varint(sock, length)

    return length, packet_ident


### Main code

def get_status(addr, port=25565):
    ### 1st pass - get the protocol version
    sock = socket.create_connection((addr, port), 10)  # Connect to the server
    sock.send(b"\x06\x00\x00\x00\x00\x00\x01")  # Send handshake packet
    sock.send(b"\x01\x00")  # Send req packet

    length, _ = read_header(sock)  # Read res packet header
    length, _ = read_varint(sock, length)  # Read res json length
    status = json.loads(read(sock, length))  # Read res json
    ver = int(status["version"]["protocol"])  # Set protocol ver for 2nd pass

    ### 2nd pass - check online mode
    sock = socket.create_connection((addr, port), 10)  # Connect to server
    sock.send(b"\x06\x00%s\x00\x00\x00\x02" % chr(ver).encode())  # Send handshake
    sock.send(b"\x03\x00\x01\x5f")  # Send login start
    # print(length, status, ver)

    return status

class scanner:
    def __int__(self):
        pass

    def player(self, file):
        db = dbManeger.dbManeger(file)
        nr = db.execute('SELECT MAX(nr) FROM ip')[0][0]
        for i in range(1, nr):
            ip = db.execute(f'SELECT ip FROM ip WHERE nr = {str(i)}')[0][0]
            port = db.execute(f'SELECT port FROM ip WHERE nr = {str(i)}')[0][0]
            print(i)
            print(ip)
            try:
                server = JavaServer.lookup(f'{ip}:{port}')
                query = server.query()
                players = query.players.names
                print(players)
                db.execute(f'UPDATE ip SET players = "{players}" WHERE nr = {str(i)}')
            except TimeoutError:
                print("Not responding")
            except ConnectionResetError:
                print("Connection closed")
            except Exception:
                print("Error")

            print("\n")
            print("-----------------------")
            print("\n")

    def plugins(self, file):
        db = dbManeger.dbManeger(file)
        nr = db.execute('SELECT MAX(nr) FROM ip')[0][0]
        for i in range(1000, nr):
            ip = db.execute(f'SELECT ip FROM ip WHERE nr = {str(i)}')[0][0]
            port = db.execute(f'SELECT port FROM ip WHERE nr = {str(i)}')[0][0]
            print(i)
            print(ip)
            try:
                server = JavaServer.lookup(f'{ip}:{port}')
                query = server.query()
                plugins = query.raw.get("plugins")
                print(plugins)
                db.execute(f'UPDATE ip SET plugins = "{plugins}" WHERE nr = {str(i)}')
            except TimeoutError:
                print("Not responding")
            except ConnectionResetError:
                print("Connection closed")
            except Exception:
                print("Error")

            print("\n")
            print("-----------------------")
            print("\n")


    def update(self, file):
        db = dbManeger.dbManeger(file)
        nr = db.execute('SELECT MAX(nr) FROM ip')[0][0]
        x = nr
        bar = Bar('Processing', max=nr)
        for i in range(1, nr):
            ip = db.execute(f'SELECT ip FROM ip WHERE nr = {str(i)}')[0][0]
            port = db.execute(f'SELECT port FROM ip WHERE nr = {str(i)}')[0][0]
            print(i)
            print(ip)
            try:
                print(get_status(ip, port))
            except:
                print("Server Offline")

            try:
                response = requests.get(f"https://geolocation-db.com/json/{ip}&position=true").json()
                country = response['country_name']
                db.execute(f'UPDATE ip SET country = "{country}" WHERE nr = {str(i)}')
                print(country)
            except:
                print("Location not found")

            try:
                server = JavaServer.lookup(f'{ip}:{port}')
                query = server.query()
                plugins = query.raw.get("plugins")
                print(plugins)
                db.execute(f'UPDATE ip SET plugins = "{plugins}" WHERE nr = {str(i)}')
                players = query.players.names
                print(players)
                db.execute(f'UPDATE ip SET players = "{players}" WHERE nr = {str(i)}')
                motd = query.motd
                print(motd)
                db.execute(f'UPDATE ip SET motd = "{motd}" WHERE nr = {str(i)}')
                onlinePlayers = query.raw.get("numplayers")
                print(onlinePlayers)
                db.execute(f'UPDATE ip SET onlinePlayers = "{onlinePlayers}" WHERE nr = {str(i)}')
                maxPlayers = query.raw.get("maxplayers")
                print(maxPlayers)
                db.execute(f'UPDATE ip SET maxPlayers = "{maxPlayers}" WHERE nr = {str(i)}')
                type = query.raw.get("gametype")
                print(type)
                db.execute(f'UPDATE ip SET type = "{type}" WHERE nr = {str(i)}')
                ping = round(server.ping())
                print(ping)
                db.execute(f'UPDATE ip SET ping = "{ping}" WHERE nr = {str(i)}')
                time_now = time.strftime("%d %b %H:%M:%S")
                print(time_now)
                db.execute(f'UPDATE ip SET last_online = "{time_now}" WHERE nr = {str(i)}')
            except TimeoutError:
                print("Not responding")
                x -= 1
            except ConnectionResetError:
                print("Connection closed")
                x -= 1
            except Exception:
                print("Error")
                x -= 1

            print("\n")
            print("-----------------------")
            print("\n")
            bar.next()
        bar.finish()
        print(x)


if __name__ == "__main__":
    s = scanner()
    while True:
        s.update(r"ip.db")
