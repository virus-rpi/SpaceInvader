from dbManeger import dbManeger


def get(file):
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


def getCLI(file):
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


def getCustom(file):
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


def remove_non_ascii(string):
    return ''.join(char for char in string if ord(char) < 128)


def add(file, db, type="GUI"):
    if type == "GUI":
        ips = get(file)
    elif type == "CLI":
        ips = getCLI(file)
    else:
        ips = getCustom(file)
    print(ips)
    for i in range(len(ips)):
        server = ips[i]
        ip = server[0]
        port = server[1]
        maxPlayers = server[2][0]
        onlinePlayers = server[2][1]
        version = server[3]
        motd = remove_non_ascii(server[4]).replace("@", "").replace('"', "").replace("'", "")
        db.add(ip, port, maxPlayers, onlinePlayers, version, motd)
        print(ip, port, maxPlayers, onlinePlayers, version, motd)


if __name__ == "__main__":
    credentials = {
        'host': 'localhost',
        'port': '5432',
        'database': 'ip',
        'user': 'dbuser',
        'password': '123456'
    }
    db = dbManeger("postgresql", credentials)
    # add("christian.txt", db, "CLI")
