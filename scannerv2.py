import json
import socket
import requests
import time
import simplejson
import ping3
import mcrcon
import asyncio
import os
from custom_modules import dbManeger, loadEnv
from dotenv import load_dotenv

load_dotenv()


def check_rcon(host="localhost", port=25575):
    try:
        socket.create_connection((host, port), .7)
        mr = mcrcon.MCRcon(host, "password", port)
        mr.connect()
        mr.disconnect()
        return True
    except mcrcon.MCRconException:
        return True
    except ConnectionRefusedError:
        return False
    except TimeoutError:
        return False
    except ConnectionResetError:
        return False


def measure_ping_time(server_ip):
    rtt = ping3.ping(server_ip)
    if rtt is not None:
        return round(rtt * 1000, 2)
    else:
        return None


def remove_non_ascii(string):
    try:
        return ''.join(char for char in string if ord(char) < 128)
    except TypeError:
        return "Non db compatible motd"


def read(sock, n):
    A = b''
    while len(A) < n:
        A += sock.recv(n - len(A))
    return A


def read_varint(sock, remaining=0):
    A = 0
    for B in range(5):
        C = ord(sock.recv(1))
        A |= (C & 127) << 7 * B
        if not C & 128:
            return remaining - (B + 1), A


def read_header(sock, compression=False):
    B = sock
    C, A = read_varint(B)
    if compression:
        A, C = read_varint(B, A)
    A, D = read_varint(B, A)
    return A, D


def get_status(addr, port=25565):
    start_time = time.perf_counter()
    sock = socket.create_connection((addr, port), 0.7)
    end_time = time.perf_counter()
    ping = round((end_time - start_time) * 1000, 2)
    sock.send(b"\x06\x00\x00\x00\x00\x00\x01")
    sock.send(b"\x01\x00")
    length, _ = read_header(sock)
    length, _ = read_varint(sock, length)
    data = json.loads(read(sock, length))
    data['ping'] = ping
    return data


def update_type(ip_id, ip, data):
    return f'Type scan not implemented'


def update_plugin(ip_id, ip, data):
    return f'Plugin scan not implemented'


class Scanner:
    def __init__(self, db):
        self.db = db
        self.data = self.read()

    def read(self):
        return self.db.execute("SELECT * FROM ip")

    @staticmethod
    async def get_data(ip, port=25565):
        r = ''
        try:
            r = get_status(ip, port)
        except TimeoutError:
            print("   Offline", end='')
            r = 'Offline'
        except ConnectionResetError:
            print("   Connection reset", end='')
            r = 'Connection reset'
        except ConnectionRefusedError:
            print("   Connection refused", end='')
            r = 'Connection refused'
        except TypeError:
            print("   Type error", end='')
            r = 'Type error'
        return r

    def update_country(self, ip_id, ip):
        try:
            country = requests.get(f"https://geolocation-db.com/json/{ip}&position=true").json()['country_name']
            self.db.execute(f"UPDATE ip SET country = '{country}' WHERE nr = {str(ip_id)}")
        except simplejson.errors.JSONDecodeError:
            country = 'Unknown'
        return f'Country: {country}'

    def update_players(self, ip_id, ip, data, advanced):
        online_players = data['players']['online']
        self.db.execute(f'UPDATE ip SET onlinePlayers = {online_players} WHERE nr = {str(ip_id)}')
        max_online_players = data['players']['max']
        self.db.execute(f'UPDATE ip SET maxPlayers = {max_online_players} WHERE nr = {str(ip_id)}')
        if advanced:
            if 'sample' in data['players']:
                players = data['players']['sample']
                if self.db.getType() == 'sqlite':
                    self.db.execute(f"UPDATE ip SET players = '{players}' WHERE nr = {str(ip_id)}")
                elif self.db.getType() == 'postgresql':
                    self.db.execute("UPDATE ip SET players = %s WHERE nr = %s", (str(players), str(ip_id)))
                return f'({online_players}/{max_online_players}) Players: {[name["name"] for name in players]}'
            else:
                self.db.execute(f"UPDATE ip SET players = '{[]}' WHERE nr = {str(ip_id)}")
                return f'({online_players}/{max_online_players}) \nPlayer names could not be retrieved'
        else:
            return f'({online_players}/{max_online_players})'

    def update_version(self, ip_id, ip, data):
        try:
            version = data['version']['name']
            self.db.execute(f"UPDATE ip SET version = '{version}' WHERE nr = {str(ip_id)};")
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
        self.db.execute(f"UPDATE ip SET motd = '{motd}' WHERE nr = {str(ip_id)}")
        return f'Motd: {motd}'

    def update_ping(self, ip_id, data):
        ping = data['ping']
        self.db.execute(f"UPDATE ip SET ping = CAST('{str(ping)}' AS float) WHERE nr = {str(ip_id)}")
        return f'Ping: {ping}'

    def update_last_online(self, ip_id):
        time_now = time.strftime("%d %b %H:%M:%S")
        self.db.execute(f"UPDATE ip SET last_online = '{time_now}' WHERE nr = {str(ip_id)}")

    def update_rcon(self, ip_id, ip):
        rcon = check_rcon(ip, 25575)
        self.db.execute(f"UPDATE ip SET rcon = '{rcon}' WHERE nr = {str(ip_id)}")
        return f'Rcon: {rcon}'

    def update_type(self, ip_id, ip, data):
        return f'Type scan not implemented'

    def update_plugin(self, ip_id, ip, data):
        return f'Plugin scan not implemented'

    def update_timeline(self, ip_id, data):
        time_now = time.strftime("%d %b %H:%M:%S")
        timeline = eval(self.db.execute(f'SELECT timeline FROM ip WHERE nr = {str(ip_id)}')[0][0])
        timeline[time_now] = json.dumps(data)
        if self.db.getType() == 'sqlite':
            self.db.execute('UPDATE ip SET timeline = ? WHERE nr = ?', (str(timeline), str(ip_id)))
        elif self.db.getType() == 'postgresql':
            self.db.execute('UPDATE ip SET timeline = %s WHERE nr = %s', (str(timeline), str(ip_id)))

    def join_server(self, ip_id, ip, port):
        requests.get(f'http://localhost:25567/connect?ip={ip}&port={port}')
        time.sleep(1)
        while "net.minecraft.class_412" in requests.get(f'http://localhost:25567/getScreen').text:
            time.sleep(.3)
        time.sleep(3)
        r = requests.get(f'http://localhost:25567/getDisconnectReason')
        if r.text != 'Not on a DisconnectedScreen':
            if 'white' in r.text or 'White' in r.text:
                self.db.execute(f"UPDATE ip SET whitelist = 'true' WHERE nr = {str(ip_id)}")
                requests.get(f'http://localhost:25567/disconnect')
                return f'Whitelist active'
        r = requests.get(f'http://localhost:25567/getScreen')
        if r.status_code == 404:
            self.db.execute(f"UPDATE ip SET whitelist = 'false' WHERE nr = {str(ip_id)}")
            requests.get(f'http://localhost:25567/disconnect')
            return f'No whitelist'
        requests.get(f'http://localhost:25567/disconnect')

    def update_shodon(self, ip_id, ip):
        result = requests.get(f'https://internetdb.shodan.io/{ip}')
        if result.status_code == 200:
            self.db.execute(f"UPDATE ip SET shodon = '{result.text}' WHERE nr = {str(ip_id)}")
            return f'Shodon: {result.text}'

    async def update(self, advanced=False, join=False, version="1.19.4", shodon=False):
        full_data = {}
        for ip_data in self.data:
            ip_id = ip_data[0]
            ip = ip_data[1]
            port = int(ip_data[2])

            print(f'Getting data of {ip_id} ({ip}:{port})', end='')
            data = await self.get_data(ip, port)
            full_data[ip_id] = [ip, port, data]
            print('')

        for ip_id in full_data.keys():
            ip = full_data[ip_id][0]
            port = full_data[ip_id][1]
            data = full_data[ip_id][2]

            self.update_timeline(ip_id, data)

            if data != 'Offline' and data != 'Connection reset' and data != 'Connection refused' and data != 'Type error':
                print(f'Updating {ip_id} ({ip}:{port}) ')
                print(self.update_version(ip_id, ip, data))
                print(self.update_motd(ip_id, ip, data))
                print(self.update_players(ip_id, ip, data, advanced))
                print(self.update_ping(ip_id, data))
                self.update_last_online(ip_id)
                if advanced:
                    print(self.update_type(ip_id, ip, data))
                    print(self.update_country(ip_id, ip))
                    print(self.update_plugin(ip_id, ip, data))
                    print(self.update_rcon(ip_id, ip))
                if join:
                    v = self.db.execute(f'SELECT version FROM ip WHERE nr = {str(ip_id)}')[0][0]
                    if version in v:
                        print(f'Joining {ip_id} ({ip}:{port})')
                        print(self.join_server(ip_id, ip, port))
                if shodon:
                    print(self.update_shodon(ip_id, ip))
            else:
                print(f'{ip_id} ({ip}:{port}) is Offline')

            print('\n----------\n')


if __name__ == "__main__":
    env = loadEnv.load()

    dbM = dbManeger.dbManeger
    db = dbM(env['DB_TYPE'], env['DB'])
    s = Scanner(db)
    asyncio.run(s.update())
