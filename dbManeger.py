import sqlite3


class dbManeger:
    def __init__(self, db):
        self.conn = None
        self.create_connection(db)

    def create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def execute(self, cmd):
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        return cursor.fetchall()

    def add(self, ip=None, port=None, maxPlayers=None, onlinePlayers=None, version = None, motd = None, players = None):
        self.execute(f"INSERT INTO ip (ip, port, maxPlayers, onlinePlayers, version, motd, players),"
                     f" VALUES({ip}, {port}, {maxPlayers}, {onlinePlayers}, {version}, {motd}, {players});")


if __name__ == "__main__":
    db = dbManeger(r"ip.db")
    print(db.execute("SELECT * FROM ip;"))
