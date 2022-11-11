from javascript import require, On

mineflayer = require('mineflayer')

bot = mineflayer.createBot({
  'host': 'reverseshell.ploudos.me',
  'auth': 'microsoft',
  #'username': 'drone'
})


print("Started mineflayer")

@On(bot, 'spawn')
def handle(*args):
  print("I spawned 👋")

@On(bot, "end")
def handle(*args):
  print("Bot ended!", args)
