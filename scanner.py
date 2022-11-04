import dbManeger
from mcstatus import JavaServer
import time
import requests


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
        for i in range(1, nr):
            ip = db.execute(f'SELECT ip FROM ip WHERE nr = {str(i)}')[0][0]
            port = db.execute(f'SELECT port FROM ip WHERE nr = {str(i)}')[0][0]
            print(i)
            print(ip)

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
        print(x)


if __name__ == "__main__":
    s = scanner()
    while True:
        s.update(r"ip.db")
