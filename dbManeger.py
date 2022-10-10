import sqlite3
from sqlite3 import Error


class dbManeger:
    def __init__(self, db):
        self.db = db
        self.conn = None
        self.cursor = None

    def create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def closeCon(self):
        self.conn.commit()
        self.cursor.close()

    def execute(self, cmd):
        self.create_connection(self.db)
        self.cursor = self.conn.cursor()
        self.cursor.execute(cmd)
        res = self.cursor.fetchall()
        self.closeCon()
        return res

    def add(self, ip=None, port=None, maxPlayers=None, onlinePlayers=None, version=None, motd=None, players=None):
        cmd = f"INSERT INTO ip (ip, port, maxPlayers, onlinePlayers, version, motd, players) " \
              f'VALUES("{ip}", {port}, {maxPlayers}, {onlinePlayers}, "{version}", "{motd}", "{players}");'
        self.execute(cmd)

    def find(self, type="ip", subject='"localhost"'):
        cmd = f'SELECT * FROM ip WHERE {type} = {subject};'
        return self.execute(cmd)

    def delete(self, nr):
        cmd = f"DELETE FROM ip WHERE nr = {nr};"
        self.execute(cmd)
        seq = self.execute('SELECT seq FROM sqlite_sequence WHERE name = "ip"')[0][0]
        cmd = f'UPDATE sqlite_sequence SET seq = {seq-1} WHERE name = "ip"'
        self.execute(cmd)




if __name__ == "__main__":
    db = dbManeger(r"ip.db")
    # db.add("93.90.178.196", 25565, 20, 0, "1.19.2", "A Minecraft Server", "{}")
    db.add("171.5.187.206", 25565, 20, 1, "1,19,2", "", "")
    # print(db.execute("SELECT * FROM ip;"))
    # print(db.find("ip", '"93.90.178.196"'))
