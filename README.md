# SpaceInvador
## A Copenheimer like bot.

The bot can scan for Minecraft Server and can run recon on the scanned servers.
## Features
- Scanning for Minecraft Servers
- Collect data about scanned servers
- Host a Discord bot to interact with data
- Host website with Statistics and controlles

## Data that gets collected
- ip
- port
- Online Players (Name + uuid)
- Max Players
- Version
- Description
- Plugins
- Type (e.g. SMP)
- Whitelist (enabled or not)
- Ping
- Last time it was scanned
- Country
- Rcon Port usable
- A timeliene of the Data
- Open Ports
- CVEs on Server
- Hostname

## Todo

- Add Minecraft bots to join all servers and collect even more data
- More Statistics
- Installer
- Add Mc bots to join server and interact with server (e.g. build schematic or chat on server)
- Proxy to connect to Servers safely and give them more abilitys through custom commands

```
 __          _______ _____    _ 
 \ \        / /_   _|  __ \  | |
  \ \  /\  / /  | | | |__) | | |
   \ \/  \/ /   | | |  ___/  | |
    \  /\  /   _| |_| |      |_|
     \/  \/   |_____|_|      (_)
```             
This Project ist still work in progress and not very useable at the moment.
Also please DON'T use it for griefing.

## Usage
1. To scan for new servers run the scan.py script, it will output a txt file with mc servers
2. Use the readFile.py script to reformat the txt file to a splite db
3. To get more information on the servers run the scaner.py script
4. To see statistics run the web_app.py script


## License
Copyright (c) 2022, virus-rpi,
All rights reserved.

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

## Credits
Satsuma for helping me with scanning for ips
