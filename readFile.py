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
                on, max = split[2].split('/')
                split[2] = [max, on]
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
                on, max = split[2].split('/')
                split[2] = [max, on]
                list.append(split)
            return list

    def getCustom(self, file):
        with open(file, encoding='utf-8') as f:
            lines = f.readlines()
            list = []
            counter = 0
            for i in lines:
                if i.strip('\n') == "Json not readable":
                    counter = 4
                if counter == 0:
                    ip, port = i.strip('\n').split(":")
                if counter == 1:
                    version = i.strip('\n').replace('Version: ', '')
                if counter == 2:
                    onlinePlayers, maxPlayers = i.strip('\n').replace("Online: ", "").split("/")
                if counter == 3:
                    motd = i.strip('\n').replace("MOTD: ", "").replace("]", "").replace("[", "")
                if counter == 4:
                    pass
                if counter == 5:
                    counter = -1
                    list.append([ip, port, [maxPlayers, onlinePlayers], version, motd])
                counter += 1
        return list



    def remove_non_ascii(self, string):
        return ''.join(char for char in string if ord(char) < 128)

    def add(self, file, dbfile, type="GUI"):
        if type == "GUI":
            ips = self.get(file)
        elif type == "CLI":
            ips = self.getCLI(file)
        else:
            ips = self.getCustom(file)
        print(ips)

        for i in range(len(ips)):
            server = ips[i]
            ip = server[0]
            port = server[1]
            maxPlayers = server[2][0]
            onlinePlayers = server[2][1]
            version = server[3]
            motd = self.remove_non_ascii(server[4]).replace("@", "").replace('"', "").replace("'", "")

            db = dbManeger.dbManeger(dbfile)
            # db.add(ip, port, maxPlayers, onlinePlayers, version, motd)


if __name__ == "__main__":
    r = readFile()
    r.add("outputs/5.txt", "ip.db", "Custom")
