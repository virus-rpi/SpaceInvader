import connect
import subprocess
import os


ip = "93.186.198.89"
port = "-p 25565"

def check(ip, port):
    proc = subprocess.Popen(f'python connect.py {ip} -p {port}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    print(f'Answer: {proc.communicate()[0]}')

ip = "93.186.198.89"
port = "25565"

check(ip, port)

ip = "93.186.205.125"
port = "25565"

check(ip, port)
