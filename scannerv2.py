import json
import socket
import dbManeger
import requests
import time
import simplejson


def remove_non_ascii(string):
    return ''.join(char for char in string if ord(char) < 128)

def read(sock, n):
    A = b''
    while len(A) < n: A += sock.recv(n - len(A))
    return A


def read_varint(sock, remaining=0):
    A = 0
    for B in range(5):
        C = ord(sock.recv(1))
        A |= (C & 127) << 7 * B
        if not C & 128: return remaining - (B + 1), A


def read_header(sock, compression=False):
    B = sock
    C, A = read_varint(B)
    if compression: A, C = read_varint(B, A)
    A, D = read_varint(B, A)
    return A, D


def get_status(addr, port=25565):
    sock = socket.create_connection((addr, port), 0.7)
    sock.send(b"\x06\x00\x00\x00\x00\x00\x01")
    sock.send(b"\x01\x00")
    length, _ = read_header(sock)
    length, _ = read_varint(sock, length)
    return json.loads(read(sock, length))


class Scanner:
    def __init__(self, file):
        self.db = dbManeger.dbManeger(file)
        self.data = self.read()

    def read(self):
        return self.db.execute("SELECT * FROM ip")

    @staticmethod
    def get_data(ip, port=25565):
        try:
            return get_status(ip, port)
        except TimeoutError:
            print("Offline")
            return 'Offline'
        except ConnectionResetError:
            print("Connection reset")
            return 'Connection reset'
        except ConnectionRefusedError:
            print("Connection refused")
            return 'Connection refused'
        except TypeError:
            print("Type error")
            return 'Type error'

    def update_country(self, ip_id, ip):
        try:
            country = requests.get(f"https://geolocation-db.com/json/{ip}&position=true").json()['country_name']
            self.db.execute(f'UPDATE ip SET country = "{country}" WHERE nr = {str(ip_id)}')
        except simplejson.errors.JSONDecodeError:
            country = 'Unknown'
        return f'Country: {country}'

    def update_players(self, ip_id, ip, data):
        online_players = data['players']['online']
        self.db.execute(f'UPDATE ip SET onlinePlayers = {online_players} WHERE nr = {str(ip_id)}')
        max_online_players = data['players']['max']
        self.db.execute(f'UPDATE ip SET maxPlayers = {max_online_players} WHERE nr = {str(ip_id)}')
        if 'sample' in data['players']:
            players = data['players']['sample']
            self.db.execute(f'UPDATE ip SET players = "{players}" WHERE nr = {str(ip_id)}')
            return f'({online_players}/{max_online_players}) Players: {[name["name"] for name in players]}'
        else:
            return f'({online_players}/{max_online_players}) \nPlayer names could not be retrieved because non Vanilla version is in use'

    def update_version(self, ip_id, ip, data):
        try:
            version = data['version']['name']
            self.db.execute(f'UPDATE ip SET version = "{version}" WHERE nr = {str(ip_id)}')
            return f'Version: {version}'
        except KeyError:
            print(data)
        except TypeError:
            print(data)

    def update_motd(self, ip_id, ip, data):
        try:
            motd = data['description']['text']
            if motd == '':
                motd = data['description']['extra'][0]['text']
        except:
            try:
                motd = motd = data['description']['extra'][0]['text']
            except:
                motd = data['description']

        motd = remove_non_ascii(motd).replace("@", "").replace('"', "").replace("'", "")
        self.db.execute(f'UPDATE ip SET motd = "{motd}" WHERE nr = {str(ip_id)}')
        return f'Motd: {motd}'

    def update_plugin(self, ip_id, ip, data):
        return f'Plugin scan not implemented'

    def update_type(self, ip_id, ip, data):
        return f'Type scan not implemented'

    def update_ping(self, ip_id, ip, data):
        return f'Ping scan not implemented'

    def update_last_online(self, ip_id):
        time_now = time.strftime("%d %b %H:%M:%S")
        self.db.execute(f'UPDATE ip SET last_online = "{time_now}" WHERE nr = {str(ip_id)}')

    def update(self):
        for ip_data in self.data:
            ip_id = ip_data[0]
            ip = ip_data[1]
            port = ip_data[2]

            print(f'Updating {ip_id} ({ip}:{port}) ')

            data = self.get_data(ip, port)

            if data != 'Offline' and data != 'Connection reset' and data != 'Connection refused' and data != 'Type error':
                print(self.update_type(ip_id, ip, data))
                print(self.update_ping(ip_id, ip, data))
                print(self.update_version(ip_id, ip, data))
                print(self.update_motd(ip_id, ip, data))
                print(self.update_players(ip_id, ip, data))
                print(self.update_country(ip_id, ip))
                print(self.update_plugin(ip_id, ip, data))
                self.update_last_online(ip_id)

            print('\n----------\n')


if __name__ == "__main__":
    # json_object = json.dumps(get_status("178.32.249.234", 25565), indent=4)
    # with open("test.json", "w") as f:
    #    f.write(json_object)
    s = Scanner(r"ip2.db")
    s.update()
