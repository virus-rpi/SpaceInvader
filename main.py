import os
import time
import setup
from custom_modules import loadEnv
import threading
import subprocess
import web_app
import datetime
from custom_modules import dbManeger
import pyperclip
from scannerv2 import Scanner
from custom_modules import discord_bot
from custom_modules import watcher

banner = r"""
  ___________________  _____  _________ ___________.___ ___________   _________  ________   ________ __________ 
 /   _____/\______   \/  _  \ \_   ___ \\_   _____/|   |\      \   \ /   /  _  \ \______ \  \_____  \\______   \
 \_____  \  |     ___/  /_\  \/    \  \/ |    __)_ |   |/   |   \   Y   /  /_\  \ |    |  \  /   |   \|       _/
 /        \ |    |  /    |    \     \____|        \|   /    |    \     /    |    \|    `   \/    |    \    |   \
/_______  / |____|  \____|__  /\______  /_______  /|___\____|__  /\___/\____|__  /_______  /\_______  /____|_  /
        \/                  \/        \/        \/             \/              \/        \/         \/       \/ 

"""

printed_servers = []


def help_cmd(args=None, env=None):
    string = "Commands:\n"
    for command in commands:
        string += f"  {command}: \n    Description: {commands[command]['description']} \n    Usage: {commands[command]['usage']}\n"
    print(string)


def scan_cmd(args=None, env=None):
    print("Scanning for new servers...\n")
    subprocess.Popen(f'python scan.py', shell=False)


def webApp_cmd(args=None, env=None):
    print("Starting web app...\n")
    subprocess.Popen(f'python web_app.py', shell=False)


def server_cmd(args=None, env=None):
    minutes = 5
    version = None
    online_players = False
    number = 1
    copy_to_clipboard = False
    ensure_no_whitelist = False
    update = False

    if args:
        for i in args:
            if i.startswith("v"):
                version = i.split(" ")[1]
            if i.startswith("o"):
                online_players = True
            if i.startswith("m"):
                minutes = int(i.split(" ")[1])
            if i.startswith("n"):
                number = i.split(" ")[1]
                if number == "all":
                    number = 999999
                else:
                    number = int(number)
            if i == "c":
                copy_to_clipboard = True
            if i == "u":
                update = True
            if i.startswith("w"):
                ensure_no_whitelist = True

    db = dbManeger.dbManeger(env['DB_TYPE'], env['DB'])
    print(f"Getting servers online in the last {minutes} minutes...")
    current_time = datetime.datetime.now()

    sql = f"SELECT * FROM ip WHERE whitelist IS NOT true"

    if online_players and version:
        sql += f" AND \"onlinePlayers\" > 0 AND version = '{version}'"
    elif online_players:
        sql += " AND \"onlinePlayers\" > 0"
    elif version:
        sql += f" AND version = '{version}'"

    servers = db.execute(sql)

    if len(servers) == 0:
        print("No servers found")
        return

    server_count = 1
    for i, data in enumerate(servers):
        if i == number:
            break

        if number != "all" and data[0] in printed_servers:
            number += 1
            continue

        last_scan_time_str = data[12]
        if last_scan_time_str is None:
            number += 1
            continue
        try:
            last_scan_time = datetime.datetime.strptime(last_scan_time_str, "%d %b %Y %H:%M:%S")
        except ValueError:
            number += 1
            continue
        time_diff = (current_time - last_scan_time).total_seconds() // 60
        if time_diff >= minutes:
            number += 1
            continue
        if ensure_no_whitelist and data[10] is None:
            number += 1
            continue
        if update:
            scanner = Scanner(dbManeger.dbManeger(env['DB_TYPE'], env['DB']))
            scanner.single_update(data[0])
            data = db.execute(f"SELECT * FROM ip WHERE nr = {data[0]}")[0]
        print(
            f"Server {server_count}: {data[1]}:{data[2]} ({data[5]})    ID: {data[0]}    Last Scan: {abs(time_diff)} minutes ago",
            end=""
        )
        if data[10] is None:
            print(f"   ⚠ No whitelist scan data available", end="")
        print()

        if copy_to_clipboard and server_count == 1:
            ip_port = f"{data[1]}:{data[2]}"
            pyperclip.copy(ip_port)
            print(f"IP:Port copied to clipboard: {ip_port}")

        printed_servers.append(data[0])
        server_count += 1
    if server_count == 1:
        print("No servers found. Try increasing the minutes or removing the online players filter")


def update_cmd(args=None, env=None):
    print("Updating...")
    advanced = False
    version = None
    batch_size = None
    shodan = False

    if args:
        for i in args:
            if i.startswith("a"):
                advanced = True
            if i.startswith("j"):
                version = i.split(" ")[1]
            if i.startswith("b"):
                batch_size = int(i.split(" ")[1])
            if i.startswith("s"):
                shodan = True

    s = Scanner(dbManeger.dbManeger(env['DB_TYPE'], env['DB']))
    eval("s.run(advanced=advanced, join=" + (
        "False" if version is None else "True") + ", version=version, shodan=shodan" + (
             f", batch_size={batch_size}" if batch_size else "") + ")")


def discord_cmd(args=None, env=None):
    print("Starting discord bot...")
    discord_bot.start()


def watch_cmd(args=None, env=None):
    mode = None
    id = None
    ip = None
    player = None

    if args:
        for i in args:
            if i.startswith("id"):
                id = i.split(" ")[1]
            if i.startswith("a"):
                mode = "add"
            if i.startswith("r"):
                mode = "remove"
            if i.startswith("l"):
                mode = "list"
            if i.startswith("ip"):
                ip = i.split(" ")[1]
            if i.startswith("p"):
                player = i.split(" ")[1]

    if player is None:
        if id is None and mode != "list":
            db = dbManeger.dbManeger(env['DB_TYPE'], env['DB'])
            id = db.execute(f"SELECT nr FROM ip WHERE ip = '{ip}' LIMIT 1")
            if len(id) == 0:
                print("No server found with that ip")
                return
            id = id[0][0]

    if mode is None:
        print("No mode specified")
        return

    if mode == "add":
        with open("watchlist", "w") as f:
            f.write(f"{id if id else player}\n")
    elif mode == "remove":
        with open("watchlist", "r") as f:
            lines = f.readlines()
        with open("watchlist", "w") as f:
            for line in lines:
                if line.strip("\n") != (id if id else player) and id != "all":
                    f.write(line)
    elif mode == "list":
        with open("watchlist", "r") as f:
            lines = f.readlines()
        for line in lines:
            print(line.strip("\n"))

    watcher.eye().restart()


def player_cmd(args=None, env=None):
    player_name = None
    server_ips = None

    if args:
        player_name = args[0]

    if player_name is None:
        print("No player specified")
        return

    db = dbManeger.dbManeger(env['DB_TYPE'], env['DB'])

    ids = db.execute(f"SELECT id FROM timeline WHERE data LIKE '%{player_name}%'")
    if ids:
        ids = list(set([i[0] for i in ids]))
        server_ips = []
        for i in ids:
            server_ips.append(db.execute(f"SELECT nr, ip FROM ip WHERE timeline LIKE '%{i}%'"))
        if server_ips:
            server_ips = list(set([f"ID: {i[0][0]}   IP: {i[0][1]}" for i in server_ips]))
    print(f"Player {player_name} was seen on: {server_ips}")


commands = {
    "help": {
        "description": "Show this help message",
        "usage": "help",
        "function": help_cmd,
        "run_in_thread": False,
    },
    "scan": {
        "description": "Scan for new Minecraft servers",
        "usage": "scan",
        "function": scan_cmd,
        "run_in_thread": True,
    },
    "webApp": {
        "description": "Start the web app",
        "usage": "webApp",
        "function": webApp_cmd,
        "run_in_thread": False,
    },
    "stop": {
        "description": "Stop threads",
        "usage": "stop",
        "function": lambda: None,
        "run_in_thread": False,
    },
    "server": {
        "description": "Returns a joinable server",
        "usage": "server [-v Version] [-o (should people be online)] [-m minutes (how long ago the server was online)] [-n int/all (number of servers to return)] [-c (copy to clipboard)] [-w (ensure server has no whitelist)] [-u update the data of hte current server ]",
        "function": server_cmd,
        "run_in_thread": False,
    },
    "exit": {
        "description": "Exit the program",
        "usage": "exit",
        "function": lambda: exit(0),
        "run_in_thread": False,
    },
    "update": {
        "description": "Update the data in the database",
        "usage": "update [-a (advanced)] [-j version (join server on version for whitelist scan)] [-b int (batch size)] [-s (Shodan lookup)]",
        "function": update_cmd,
        "run_in_thread": False,
    },
    "discord": {
        "description": "Start the discord bot",
        "usage": "discord",
        "function": discord_cmd,
        "run_in_thread": False,
    },
    "watchlist": {
        "description": "Put servers on the watchlist",
        "usage": "watchlist [-id id] [-a (add)] [-r (remove)] [-l (list)] [-ip ip]",
        "function": watch_cmd,
        "run_in_thread": True,
    },
    "player": {
        "description": "Get a player's name history",
        "usage": "player -<name>",
        "function": player_cmd,
        "run_in_thread": False,
    },
}


def run_command(cmd, args=None, env=None):
    if cmd in commands:
        if cmd == "stop":
            for thread in threading.enumerate():
                if thread != threading.current_thread():
                    thread.join()
            return
        else:
            if commands[cmd].get("run_in_thread", False):
                thread = threading.Thread(target=commands[cmd]["function"], args=(args, env))
                thread.start()
            else:
                commands[cmd]["function"](args, env)


def main():
    print(banner)
    env = loadEnv.load()

    if not os.path.exists('.env'):
        setup.setup()
        print("Setup complete, please restart the program")

    while True:
        user_input = input(">>> ")
        parts = user_input.split(maxsplit=1)
        cmd = parts[0]
        args = parts[1].split('-')[1:] if len(parts) > 1 else None

        if cmd in commands:
            run_command(cmd, args, env)


if __name__ == "__main__":
    main()
