import os

from readFile import readFile
from dbManeger import dbManeger
import regex as re
from dotenv import load_dotenv

load_dotenv()


DB_TYPE = os.getenv("dbType")
if DB_TYPE == "postgres":
    DB = os.getenv("credentials")
if DB_TYPE == "sqlite":
    DB = os.getenv("dbFile")


class importer:
    def __init__(self):
        self.type = None
        self.data = None
        self.db = dbManeger(DB_TYPE, DB)

    def figureOutType(self):
        if self.data.endswith(".txt"):
            with open(self.data, encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                GUIPattern = re.compile("\d+ - \d+.\d+.\d+.\d+ - \d+ - \d+/\d+ - [A-Za-z0-9. ]+- [A-Za-z0-9. ]+-")
                CLIPattern = re.compile("[(]\d+.\d+.\d+.\d+:\d+[)][(]\d+/\d+[)][(]\d+.\d+.\d+[)][(]")
                if re.search(GUIPattern, lines[0]):
                    return "GUI"
                if re.search(CLIPattern, lines[0]):
                    return "CLI"

    def importData(self, data):
        self.data = data
        self.type = self.figureOutType()
        print(f"Importing to {DB_TYPE} database...")
        # readFile(self.db, self.data, self.type).add()


if __name__ == "__main__":
    i = importer()
    i.importData("servers.txt")
