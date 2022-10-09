import dbManeger
from mcstatus import JavaServer
from multiprocessing.pool import ThreadPool as Pool


class scanner:
    def __int__(self):
        pass

    def worker(self, db, i):
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
        pool_size = nr
        pool = Pool(pool_size)
        for i in range(1, nr):
            pool.apply_async(self.worker, (db, i,))

        pool.close()
        pool.join()


if __name__ == "__main__":
    s = scanner()
    s.update(r"ip.db")
