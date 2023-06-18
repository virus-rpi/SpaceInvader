from dotenv import load_dotenv
import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

load_dotenv()


def load():
    DB_TYPE = os.getenv("dbType")
    if DB_TYPE == "postgres":
        DB = eval(os.getenv("credentials"))
    elif DB_TYPE == "sqlite":
        DB = os.getenv("dbFile")
    else:
        DB = None
    webPort = os.getenv("webPort")
    discordToken = os.getenv("discordToken")
    scanning_method = os.getenv("scanning_method")
    return {'DB_TYPE': DB_TYPE, 'DB': DB, 'webPort': webPort, 'discordToken': discordToken, 'scanning_method': scanning_method}


if __name__ == "__main__":
    print(load())
