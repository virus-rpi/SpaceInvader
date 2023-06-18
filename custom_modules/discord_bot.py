import discord
import subprocess
import os
import inspect
import sys

try:
    import custom_modules.loadEnv as loadEnv
except ImportError:
    import loadEnv
try:
    import main
except ImportError:
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
    import main

intents = discord.Intents.all()
client = discord.Client(intents=intents)
blacklisted_commands = ["update"]


class OutputCapture(object):
    def __init__(self):
        self.output = []

    def write(self, text):
        self.output.append(text)


@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("/"):
        output_capture = OutputCapture()
        sys.stdout = output_capture
        user_input = message.content.strip()[1:]
        parts = user_input.split(maxsplit=1)
        cmd = parts[0]
        args = parts[1].split('-')[1:] if len(parts) > 1 else None

        if cmd in blacklisted_commands:
            await message.channel.send("This command is not available in the discord bot.")
            return
        if cmd == "exit":
            await message.channel.send("Bot is shutting down. Goodbye!")
            sys.stdout = sys.__stdout__
            await client.close()
            return

        if cmd in main.commands:
            main.run_command(cmd, args, loadEnv.load())

        output = []
        try:
            sys.stdout = sys.__stdout__
            output = output_capture.output
        except Exception as e:
            output = ["Error: " + str(e)]
        for line in output:
            if len(line) > 0 and line != "\n":
                await message.channel.send(line)


def start():
    env = loadEnv.load()
    discordToken = env['discordToken']
    if discordToken is None:
        print("Discord bot not enabled.")
        exit(1)

    client.run(discordToken)
