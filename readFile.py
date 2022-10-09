import dbManeger

class readFile:
    def __int__(self, file="ips.txt"):
        self.get(file)

    def get(self, file):
        with open(file) as f:
            lines = f.readlines()
            list = []
            for i in lines:
                split = i.split(" - ")
                del split[0]
                del split[-1]
                split[2] = split[2].split('/')
                list.append(split)
            return list

    def getCLI(self, file):
        with open(file, encoding='utf-8') as f:
            lines = f.readlines()
            list = []
            for i in lines:
                i = i.strip("\n")
                i = i[1:]
                i = i[:-1]
                split = i.split(")(")
                ipport = split[0].split(":")
                split.pop(0)
                split.insert(0, ipport[0])
                split.insert(1, ipport[1])
                split[2] = split[2].split('/')
                list.append(split)
            return list

    def remove_non_ascii(self, string):
        return ''.join(char for char in string if ord(char) < 128)

    def add(self, file, dbfile, CLI=False):
        if CLI == False:
            ips = self.get(file)
        else:
            ips = self.getCLI(file)

        for i in range(len(ips)):
            server = ips[i]
            ip = server[0]
            port = server[1]
            maxPlayers = server[2][0]
            onlinePlayers = server[2][1]
            version = server[3]
            motd = self.remove_non_ascii(server[4]).replace("@", "").replace('"', "").replace("'", "")

            db = dbManeger.dbManeger(dbfile)
            db.add(ip, port,onlinePlayers, maxPlayers, version, motd)


if __name__ == "__main__":
    r = readFile()
    r.add("ips.txt", "ip.db")
    r.add("ips2.txt", "ip.db", True)
