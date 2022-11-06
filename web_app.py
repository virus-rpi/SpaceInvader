from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output
import dash
import dash_daq as daq
import dbManeger
import plotly.graph_objects as go

app = Dash(__name__, external_stylesheets=['https://raw.githubusercontent.com/virus-rpi/SpaceInvador/main/assets/style.css'])

app.layout = html.Div([
    html.Div([
        html.H1(
            children='Dashboard of SpaceInvador',
            style={
                'text-align': 'center',
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
                'text-align': 'center'
            }
        ),
        html.P(" \n\n\n"),
        html.H4("Statistics"),
        dcc.Graph(id="graph", style={'height': 1150}),
        html.P(" \n\n\n"),
    ],
        style={
            'background-color': '#111111',
            'textAlign': 'center',
            'margin': 'auto'
        }
    ),
    html.Div([
        html.H4(
            children="Control",
            style={
                'text-align': 'center',
            }
        ),
        html.P(" \n\n\n"),
        daq.ToggleSwitch(
            id="dc_bot",
            value=False,
            label="Discord bot:",
            labelPosition='top',
            style={
                'text-align': 'left',
            }
        ),
        html.Div(id="dc_bot_div")

    ],
        style={
            'background-color': '#111111',
        })
])


def percent(part, whole):
    return 100 * float(part) / float(whole)



@app.callback(
    Output('dc_bot_div', 'children'),
    Input('dc_bot', 'value'),
)
def toggle_bot(value):
    return value
@app.callback(
    Output("graph", "figure"),
    [dash.dependencies.Input('update', 'n_clicks')],
)
def update_charts(_):
    db = dbManeger.dbManeger(r"ip.db")

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
            [{"type": "bar"}, {"type": "pie"}]],
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


if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0')
