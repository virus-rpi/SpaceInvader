CREATE TABLE "ip" (
    "nr"            SERIAL PRIMARY KEY,
    "ip"            TEXT,
    "port"          NUMERIC,
    "onlinePlayers" INTEGER,
    "maxPlayers"    INTEGER,
    "version"       TEXT,
    "motd"          TEXT,
    "players"       TEXT,
    "plugins"       TEXT,
    "type"          TEXT,
    "whitelist"     BOOLEAN,
    "ping"          FLOAT,
    "last_online"   TEXT,
    "country"       TEXT,
    "rcon"          TEXT DEFAULT 'False',
    "timeline"      TEXT DEFAULT '{}',
    "shodon"        TEXT
);

CREATE TABLE "timeline" (
    "id"     SERIAL PRIMARY KEY,
    "timestamp" TEXT,
    "data"   TEXT
);

CREATE USER dbUser WITH PASSWORD '123456' SUPERUSER;