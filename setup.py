dbFile = None
credentials = None
discordToken = None
webPort = None

dbType = input("Enter the database type (postgres, sqlite): ")
if dbType == "postgres":
    credentials = {
        'host': input("Enter the host: "),
        'port': input("Enter the port: "),
        'database': input("Enter the database name: "),
        'user': input("Enter the username: "),
        'password': input("Enter the password: ")
    }
if dbType == "sqlite":
    dbFile = input("Enter the database file name: ")

discordBool = input("Do you want to enable discord bot? (y/n): ")
if discordBool == "y":
    discordToken = input("Enter the discord bot token: ")

webBool = input("Do you want to enable web server? (y/n): ")
if webBool == "y":
    webPort = input("Enter the web server port: ")

with open(".env", "w") as f:
    f.write(f"dbType={dbType}\n")
    if credentials:
        f.write(f"credentials={credentials}\n")
    if dbFile:
        f.write(f"dbFile={dbFile}\n")
    if discordBool == "y":
        f.write(f"discordToken={discordToken}\n")
    if webBool == "y":
        f.write(f"webPort={webPort}\n")