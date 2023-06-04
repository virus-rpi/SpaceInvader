import interactions
import os as osys
import sys
import subprocess
import json
import multiprocessing


def config_path():
    path = osys.path.dirname(osys.path.abspath(__file__))
    path = path.replace('\\', '/') + "/config.json"
    return path


if not osys.path.isfile(config_path()):
    sys.exit(f"'{config_path()}' not found! Please add it and try again.")
else:
    with open(config_path()) as file:
        config = json.load(file)

bot = interactions.Client(config['token'])


####################
# Discord commands #
####################
# Scan the large list


# Help command
@bot.command(
    name="help",
    description="Show the help message",
)
async def help(ctx: interactions.CommandContext):
    await ctx.send(
        """
########################################################
/db
gives you the db
/help
shows this message
########################################################
"""
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, bot.HTTPException):
        print("You are ratelimited")


# Startup
def startup():
    bot.start()


# Print whether debugging and testing are active
if __name__ == "__main__":
    print(f'Starting bot with token {config["token"]} and database {config["db_path"]}')
    flag = True
    proc2 = multiprocessing.Process(target=startup)
    proc2.start()
    proc2.join()
