CREATE TABLE "ip" (
    "nr" SERIAL PRIMARY KEY,
    "ip" TEXT,
    "port" NUMERIC,
    "onlinePlayers" INTEGER,
    "maxPlayers" INTEGER,
    "version" TEXT,
    "motd" TEXT,
    "players" TEXT,
    "plugins" TEXT,
    "type" TEXT,
    "whitelist" NUMERIC,
    "ping" BYTEA,
    "last_online" TEXT,
    "country" TEXT,
    "rcon" TEXT DEFAULT 'False',
    "timeline" TEXT DEFAULT '{}',
    "shodon" TEXT
);