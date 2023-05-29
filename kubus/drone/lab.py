from javascript import require, On
import time
import random


class BOT:
    def __init__(self):
        self.bot = None
        # self.got = require('got', '11.8.3')
        self.mineflayer = require('mineflayer')
        # self.thealtening = require('thealtening-free')

    def start(self):
        self.bot = self.mineflayer.createBot({
            'host': 'baum-server.de',
            'auth': 'microsoft',
            # 'username': 'drone' + str(random.randint(1, 1000000000)
            })

        print("Started mineflayer")


while True:
    b = BOT()
    b.start()


    @On(b.bot, 'spawn')
    def handle(*args):
        print("I spawned 👋")

    @On(b.bot, "end")
    def handle(*args):
        print("Bot ended!", args)


    print("____________________________")
    break
    time.sleep(5)
