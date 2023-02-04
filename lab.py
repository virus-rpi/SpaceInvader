import random
import dbManeger
from mcstatus import JavaServer
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output
import dash
import dash_daq as daq
import dbManeger
import plotly.graph_objects as go
from threading import Thread
import os
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import country_converter as coco
import numpy as np

# db = dbManeger.dbManeger(r"ip.db")
# # print(db.execute('SELECT MAX(nr) FROM ip')[0][0])
#
# server = JavaServer("93.30.211.177")
# q = server.query()
# print(q.raw)
#
# import asyncio
#
# from minecraft import Server
#
# async def main():
#     ip = "176.9.20.205"
#     port = 25565 # rcon port
#     password = ""
#
#     # can be used in a context manager
#     async with Server(ip, port, password) as server:
#         print(await server.send("list"))
#
#     # can also be used procedurally
#     server = Server(ip, port, password, connect_on_send=True)
#     # connect_on_send make it so the Server tried to reconnect if
#     # it's disconnected, otherwise it raises a NotConnectedError
#     print(await server.send("list"))
#
#     for i in await server.online():
#         print(f"{i} is online")
#
#     await server.close()
#
# asyncio.run(main())

disk_engine = create_engine('sqlite:///ip.db')

df = pd.read_sql_query('SELECT country, COUNT(*) FROM ip GROUP BY country', disk_engine)

df = df.replace(to_replace='None', value=np.nan).dropna()
df = df.replace(to_replace='Not found', value=np.nan).dropna()

for i in list(df['country']):
    print(i, coco.convert(names=[i], to="ISO2"))
    df.loc[df['country'].isin([i]), 'country'] = coco.convert(names=[i], to="ISO3")

print(df)

fig = px.scatter_geo(df, locations="country",
                     hover_name="country",
                     size="COUNT(*)",
                     # projection="natural earth",
                     color="country"
                     )
fig.show()
