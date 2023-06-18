import sqlite3
from sqlite3 import Error
import psycopg2
try:
    import loadEnv
except ModuleNotFoundError:
    import custom_modules.loadEnv as loadEnv


class dbManeger:
    def __init__(self, type, credentials):
        self.type = type
        self.credentials = credentials
        self.conn = None
        self.cursor = None

    def create_connection(self):
        if self.type == "postgres":
            try:
                self.conn = psycopg2.connect(
                    "host={host} port={port} dbname={database} user={user} password={password}".format(
                        **self.credentials))
            except psycopg2.Error as e:
                print(e)
        elif self.type == "sqlite":
            try:
                self.conn = sqlite3.connect(self.credentials)
            except Error as e:
                print(e)

    def closeCon(self):
        self.conn.commit()
        self.cursor.close()

    def execute(self, cmd, params=None):
        if not cmd.endswith(";"):
            cmd += ";"
        if self.conn is None:
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
        except Exception as e:
            print(e)
            self.closeCon()

    def add(self, ip=None, port=None, maxPlayers=None, onlinePlayers=None, version=None, motd=None, players=None):
        if self.type == "sqlite":
            cmd = "INSERT INTO ip (ip, port, maxPlayers, onlinePlayers, version, motd, players) VALUES (?, ?, ?, ?, ?, ?, ?);"
            params = (ip, port, maxPlayers, onlinePlayers, version, motd, players)
            self.execute(cmd, params)
        elif self.type == "postgres":
            cmd = "INSERT INTO ip (ip, port, maxPlayers, onlinePlayers, version, motd, players) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            params = (ip, port, maxPlayers, onlinePlayers, version, motd, players)
            self.execute(cmd, params)

    def getType(self):
        return self.type


if __name__ == "__main__":
    env = loadEnv.load()

    db = dbManeger(env['DB_TYPE'], env['DB'])
    print(db.execute("SELECT * FROM ip;"))
