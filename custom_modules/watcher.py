try:
    import loadEnv
    import dbManeger
except ImportError:
    from custom_modules import loadEnv
    from custom_modules import dbManeger

import os
import sys
import inspect
import time
import asyncio
from playsound import playsound

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

def ps():
    try:
        playsound("D:/Python/SPACEINVADOR/ping.mp3")
    except:
        pass

import scannerv2

class eye:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def restart(cls):
        cls._instance = None

    def __init__(self):
        self.env = loadEnv.load()
        self.db = dbManeger.dbManeger(self.env['DB_TYPE'], self.env['DB'])
        self.scanner = scannerv2.Scanner(self.db)
        self.onlinelist = []

        try:
            with open('watchlist') as f:
                self.watchlist = f.readlines()
        except FileNotFoundError:
            self.watchlist = ["virusrpi", "314410"]

        while True:
            self.update()
            time.sleep(5)

    def update(self):
        if not self.watchlist:
            return
        for i in self.watchlist:
            i = i.strip()
            if i:
                if i.isdigit():
                    self.check_server(i)
                else:
                    self.check_player(i)

    def check_server(self, ip_id):
        data_prev_raw = self.db.execute(f"SELECT * FROM ip WHERE nr = {ip_id}")
        with open(os.devnull, "w") as devnull:
            sys.stdout = devnull
            asyncio.run(self.scanner.single_update(int(ip_id)))
            sys.stdout = sys.__stdout__
        data_new_raw = self.db.execute(f"SELECT * FROM ip WHERE nr = {ip_id}")

        data_prev = {
            'version': data_prev_raw[0][5],
            'max_players': data_prev_raw[0][4],
            'on_players': data_prev_raw[0][3],
            'players': data_prev_raw[0][7],
            'shodan_info': data_prev_raw[0][16],
            'motd': data_prev_raw[0][6],
        }

        data_new = {
            'version': data_new_raw[0][5],
            'max_players': data_new_raw[0][4],
            'on_players': data_new_raw[0][3],
            'players': data_new_raw[0][7],
            'shodan_info': data_new_raw[0][16],
            'motd': data_new_raw[0][6],
        }

        if data_prev['version'] != data_new['version']:
            print(f"Server {ip_id}: Version changed: {data_prev['version']} -> {data_new['version']}")
            ps()

        if data_prev['max_players'] != data_new['max_players']:
            print(f"Server {ip_id}: Max players changed: {data_prev['max_players']} -> {data_new['max_players']}")
            ps()

        if data_prev['on_players'] != data_new['on_players']:
            print(f"Server {ip_id}: Online players changed: {data_prev['on_players']} -> {data_new['on_players']}")
            ps()

        prev_players = [player['name'] for player in eval(data_prev['players'])].sort()
        new_players = [player['name'] for player in eval(data_new['players'])].sort()
        if prev_players != new_players:
            print(f"Server {ip_id}: Players changed ({len(prev_players)} -> {len(new_players)}): {prev_players} -> {new_players}")
            ps()

        if data_prev['shodan_info'] != data_new['shodan_info']:
            print(f"Server {ip_id}: Shodan info changed: {data_prev['shodan_info']} -> {data_new['shodan_info']}")
            ps()

        if data_prev['motd'] != data_new['motd']:
            print(f"Server {ip_id}: Motd changed: {data_prev['motd']} -> {data_new['motd']}")
            ps()

    def check_player(self, player_name):
        ids = self.db.execute(f"SELECT nr FROM ip WHERE players LIKE '%{player_name}%'")
        if ids:
            if player_name not in self.onlinelist:
                self.onlinelist.append(player_name)
                print(f"Player {player_name} found in {len(ids)} servers: {ids}")
                ps()
        else:
            if player_name in self.onlinelist:
                self.onlinelist.remove(player_name)
                print(f"Player {player_name} went offline")
                ps()


if __name__ == "__main__":
    eye().restart()
