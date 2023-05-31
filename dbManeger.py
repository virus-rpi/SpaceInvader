import sqlite3
from sqlite3 import Error
import psycopg2


class dbManeger:
    def __init__(self, type, cerdentials):
        self.type = type
        self.cerdentials = cerdentials
        self.conn = None
        self.cursor = None

    def create_connection(self):
        if self.type == "postgresql":
            try:
                self.conn = psycopg2.connect("host={host} port={port} dbname={database} user={user} password={password}".format(**self.cerdentials))
            except psycopg2.Error as e:
                print(e)
        elif self.type == "sqlite":
            try:
                self.conn = sqlite3.connect(self.cerdentials)
            except Error as e:
                print(e)

    def closeCon(self):
        self.conn.commit()
        self.cursor.close()

    def execute(self, cmd, params=None):
        if not cmd.endswith(";"):
            cmd += ";"
        self.create_connection()
        self.cursor = self.conn.cursor()
        if params is None:
            self.cursor.execute(cmd)
        else:
            self.cursor.execute(cmd, params)
        try:
            res = self.cursor.fetchall()
            self.closeCon()
            return res
        except:
            self.closeCon()

    def add(self, ip=None, port=None, maxPlayers=None, onlinePlayers=None, version=None, motd=None, players=None):
        if self.type == "sqlite":
            cmd = "INSERT INTO ip (ip, port, maxPlayers, onlinePlayers, version, motd, players) VALUES (?, ?, ?, ?, ?, ?, ?);"
            params = (ip, port, maxPlayers, onlinePlayers, version, motd, players)
            self.execute(cmd, params)
        elif self.type == "postgresql":
            cmd = "INSERT INTO ip (ip, port, maxPlayers, onlinePlayers, version, motd, players) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            params = (ip, port, maxPlayers, onlinePlayers, version, motd, players)
            self.execute(cmd, params)

    def find(self, type="ip", subject='"localhost"'):
        cmd = f'SELECT * FROM ip WHERE {type} = {subject};'
        return self.execute(cmd)

    def delete(self, nr):
        cmd = f"DELETE FROM ip WHERE nr = {nr};"
        self.execute(cmd)
        seq = self.execute('SELECT seq FROM sqlite_sequence WHERE name = "ip"')[0][0]
        cmd = f'UPDATE sqlite_sequence SET seq = {seq-1} WHERE name = "ip"'
        self.execute(cmd)

    def getType(self):
        return self.type


if __name__ == "__main__":
    credentials = {
        'host': 'localhost',
        'port': '5432',
        'database': 'ip',
        'user': 'dbuser',
        'password': '123456'
    }
    db = dbManeger("postgresql", credentials)
    print(db.find("nr", '"1"'))
