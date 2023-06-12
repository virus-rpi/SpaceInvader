from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output
import dash
import dash_daq as daq
from custom_modules import dbManeger
import plotly.graph_objects as go
from threading import Thread
import os
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import country_converter as coco
import numpy as np
from custom_modules import loadEnv

# from bot import bot

app = Dash(__name__,
           external_stylesheets=['https://raw.githubusercontent.com/virus-rpi/SpaceInvador/main/assets/style.css']
           )


def globe():
    env = loadEnv.load()

    if env['DB_TYPE'] == 'sqlite':
        disk_engine = create_engine(f'sqlite:///{env["DB"]}')
        df = pd.read_sql_query('SELECT country, COUNT(*) FROM ip GROUP BY country', disk_engine)

        df = df.replace(to_replace='None', value=np.nan).dropna()
        df = df.replace(to_replace='Not found', value=np.nan).dropna()

        for i in list(df['country']):
            # print(i, coco.convert(names=[i], to="ISO2"))
            df.loc[df['country'].isin([i]), 'country'] = coco.convert(names=[i], to="ISO3")

        fig = px.scatter_geo(df, locations="country",
                             hover_name="country",
                             size="COUNT(*)",
                             # projection="natural earth",
                             color="country"
                             )
        fig.update_layout(template="plotly_dark")
        return fig
    else:
        return 'Not supported for this dbType'


app.layout = html.Div([
    html.Div([
        html.H1(
            children='Dashboard of SpaceInvador',
            style={
                'textAlign': 'center',
		'color': 'white'
            }
        ),
        html.P(
            children="Click here to update:",
            style={
                'color': 'white',
            }
        ),
        html.Button(
            "Update",
            id="update",
            style={
                'textAlign': 'center',
		'color': 'white'
            }
        ),
        html.P(" \n\n\n"),
        html.H4(
	    children="Statistics",
	    style={
		'color': 'white',
            }
	),
        dcc.Graph(id="graph", style={'height': 1150}),
        html.P(" \n\n\n"),
        html.H4(
	    children="Map",
	    style={
		'color': 'white',
            }
	),
        # dcc.Graph(figure=globe()),
        html.P(" \n\n\n"),
    ],
        style={
            'backgroundColor': '#111111',
            'textAlign': 'center',
            'margin': 'auto'
        }
    ),
    html.Div([
        html.H4(
            children="Control",
            style={
                'textAlign': 'center',
		'color': 'white',
            }
        ),
        html.P(" \n\n\n"),
        daq.ToggleSwitch(
            id="dc_bot",
            value=False,
            label="Discord bot:",
            labelPosition='top',
            style={
                'textAlign': 'left',
		'color': 'white',
            }
        ),
        html.Div(id="dc_bot_div"),
    ],
        style={
            'backgroundColor': '#111111',
        })
])


def percent(part, whole):
    return 100 * float(part) / float(whole)


# t = bot.bot_class('T')


@app.callback(
    Output('dc_bot_div', 'children'),
    Input('dc_bot', 'value'),
)
def toggle_bot(value):
    print(value)
    if value:
        print('Try to start bot')
        # t.start()
        print('Started bot')
    if not value:
        try:
            # t.stop()
            # t.join()
            print('Stopped bot')
        except Exception as e:
            print(e)
    return value


@app.callback(
    Output("graph", "figure"),
    [dash.dependencies.Input('update', 'n_clicks')],
)
def update_charts(_):
    env = loadEnv.load()

    db = dbManeger.dbManeger(env['DB_TYPE'], env['DB'])

    countrys = db.execute('SELECT country FROM ip')

    for j, i in enumerate(countrys):
        countrys[j] = i[0]

    labels1 = list(dict.fromkeys(countrys))

    dic = dict((x, countrys.count(x)) for x in set(labels1))
    c = sum(list(dic.values()))

    other = 0

    for i in dic.values():
        if percent(i, c) < 1:
            other += i
            dic = {key: val for key, val in dic.items() if val != i}

    dic["Other"] = other

    values1 = list(dic.values())
    labels1 = list(dic.keys())
    if None in labels1:
        i = labels1.index(None)
        labels1 = labels1[:i] + ['Offline'] + labels1[i + 1:]

    versions = db.execute('SELECT version FROM ip')

    for j, i in enumerate(versions):
        versions[j] = i[0]

    labels2 = list(dict.fromkeys(versions))

    dic = dict((x, versions.count(x)) for x in set(labels2))
    c = sum(list(dic.values()))

    other = 0

    for i in dic.values():
        if percent(i, c) < 3:
            other += i
            dic = {key: val for key, val in dic.items() if val != i}

    dic["Other"] = other

    values2 = list(dic.values())
    labels2 = list(dic.keys())

    ping = db.execute('SELECT ping FROM ip')
    for j, i in enumerate(ping):
        ping[j] = i[0]
    ping = [a for a in ping if a is not None]

    x = list(range(1, len(ping)))

    motd = db.execute('SELECT motd FROM ip')
    for j, i in enumerate(motd):
        motd[j] = i[0]
    a = motd.count("A Minecraft Server")
    b = len(motd) - a
    labels3 = ['Motd: "A Minecraft Server"', 'Motd: Not "A Minecraft Server"']
    values3 = [a, b]

    try:
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Country\n",
                "Version\n",
                f'Ping (Avg: {int(sum(ping) / len(ping))})\n',
                "Motd\n"
            ),
            specs=[
                [{"type": "pie"}, {"type": "pie"}],
                [{"type": "bar"}, {"type": "pie"}],
            ],
        )
    except ZeroDivisionError:
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Country\n",
                "Version\n",
                'Ping not found\n',
                "Motd\n"
            ),
            specs=[
                [{"type": "pie"}, {"type": "pie"}],
                [{"type": "bar"}, {"type": "pie"}],
            ],
        )

    fig.add_trace(
        go.Pie(labels=labels1, values=values1),
        row=1, col=1
    )
    fig.add_trace(
        go.Pie(labels=labels2, values=values2),
        row=1, col=2
    )

    fig.add_trace(
        go.Bar(x=x, y=ping),
        row=2, col=1
    )

    fig.add_trace(
        go.Pie(labels=labels3, values=values3),
        row=2, col=2
    )

    fig.update_layout(template="plotly_dark")

    return fig


def run():
    env = loadEnv.load()
    if env['webPort']:
        app.run_server(debug=True, port=int(env['webPort']), host='localhost')
    else:
        print('Web server disabled')


if __name__ == "__main__":
    run()
