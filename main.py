import os
import time
import setup
from custom_modules import loadEnv
import threading
import subprocess

banner = """
"""
print(banner)

if not os.path.exists('.env'):
    setup.setup()
    print("Setup complete, please restart the program")

env = loadEnv.load()


def help_cmd():
    string = "Commands:\n"
    for command in commands:
        string += f"  {command}: \n    Description: {commands[command]['description']} \n    Usage: {commands[command]['usage']}\n"
    print(string)


def scan_cmd():
    print("Scanning for new servers...\n")
    subprocess.Popen(f'python scan.py', shell=False)


def run_command(cmd):
    if cmd in commands:
        if cmd == "stop":
            stop_flag.set()
        else:
            if commands[cmd].get("run_in_thread", False):
                thread = threading.Thread(target=commands[cmd]["function"])
                thread.start()
            else:
                commands[cmd]["function"]()


commands = {
    "help": {
        "description": "Show this help message",
        "usage": "help",
        "function": help_cmd,
        "run_in_thread": False,
    },
    "scan": {
        "description": "Scan for new Minecraft server",
        "usage": "scan",
        "function": scan_cmd,
        "run_in_thread": False,
    },
}

while True:
    cmd = input(">>> ")
    if cmd in commands:
        run_command(cmd)
