import os

# Get the absolute path of the current script
script_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)
os.system("npm install mineflayer")
os.system(f"node {script_path}/whitelist_bot.js")
