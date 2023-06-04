""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.2.1
"""

from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks
import discord
import os
import sys
import json


def config_path():
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = path.replace('\\', '/') + "/config.json"
    return path


if not os.path.isfile(config_path()):
    sys.exit(f"'{config_path()}' not found! Please add it and try again.")
else:
    with open(config_path()) as file:
        config = json.load(file)


# Here we name the cog and create a new class for the cog.
class Bot(commands.Cog, name="bot"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="db",
        description="Gets you the db",
    )

    async def db(self, ctx):
        """
        Gets the database
        """
        await ctx.send(file=discord.File(config['db_path']))


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Bot(bot))
