# SpaceInvador
## A Copenheimer like bot.

The bot can scan for Minecraft Server and can run recon on the scanned servers.
## Features
- Scanning for Minecraft Servers
- Collect data about scanned servers
- Host a Discord bot to interact with data (Deleted)
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
- Dockerizaton
- Add Mc bots to join server and interact with server (e.g. build schematic or chat on server)
- Proxy to connect to Servers safely and give them more abilitys through custom commands
- Reimplement Discord Bot

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
1. Setup the DB
2. Run the setup.py script and answer the questions
3. To scan for server ips run scan.py
4. To update the DB and collect more data run scannerV2.py
5. To see stats run web_app.py


## How to setup the Database
### Sqlite:
1. Rename the templatDB.db file to anything you like
### Postgres:
1. Edit the username, password and db name in the Dockerfile
2. Build the Docker Container with:
   ```
   docker build -t spaceinvador-image .
   ```
3. Run the Docker Container with:
   ```
   docker run -d --name spaceinvador-container -p 5432:5432 spaceinvador-image
   ```


## License
Copyright (c) 2023, virus-rpi,
All rights reserved.

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

## Credits
Satsuma for helping me with scanning for ips
