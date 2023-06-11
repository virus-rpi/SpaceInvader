from dotenv import load_dotenv
import os

load_dotenv()


def load():
    DB_TYPE = os.getenv("dbType")
    if DB_TYPE == "postgres":
        DB = os.getenv("credentials")
    if DB_TYPE == "sqlite":
        DB = os.getenv("dbFile")
    else:
        DB = None
    webPort = os.getenv("webPort")
    discordToken = os.getenv("discordToken")
    return {'DB_TYPE': DB_TYPE, 'DB': DB, 'webPort': webPort, 'discordToken': discordToken}


if __name__ == "__main__":
    print(load())
