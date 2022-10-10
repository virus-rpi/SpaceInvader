import dbManeger
from mcstatus import JavaServer
from multiprocessing.pool import ThreadPool as Pool
import time


class scanner:
    def __int__(self):
        self.done = 0

    def worker(self, db, i, nr):
        x = nr
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
        except TimeoutError:
            print("Not responding")
            x -= 1
        except ConnectionResetError:
            print("Connection closed")
            x -= 1
        except Exception as e:
            print("Error")
            print(str(e))
            x -= 1
        finally:
            self.done += 1
            print("Done!")

        print("\n")
        print("-----------------------")
        print("\n")

    def update(self, file):
        self.done = 0
        db = dbManeger.dbManeger(file)
        nr = db.execute('SELECT MAX(nr) FROM ip')[0][0]
        pool = Pool(3)
        for i in range(1, nr):
            pool.apply_async(self.worker, (db, i, nr,))
        pool.close()
        pool.join()


if __name__ == "__main__":
    s = scanner()
    while True:
        print(
            "   _____ _______       _____ _______ \n  / ____|__   __|/\   |  __ \__   __|\n | (___    | |  /  \  | |__) | | |   \n  \___ \   | | / /\ \ |  _  /  | |   \n  ____) |  | |/ ____ \| | \ \  | |   \n |_____/   |_/_/    \_\_|  \_\ |_|  \n ")
        s.update(r"ip.db")
        print(
            " _____   ____  _   _ ______ \n|  __ \ / __ \| \ | |  ____|\n| |  | | |  | |  \| | |__   \n| |  | | |  | | . ` |  __|  \n| |__| | |__| | |\  | |____ \n|_____/ \____/|_| \_|______|\n")
