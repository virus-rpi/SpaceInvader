import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dbManeger


def percent(part, whole):
    return 100 * float(part)/float(whole)


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
labels1 = labels1[:i]+['Offline']+labels1[i+1:]


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

values2 = list(dic.values())
labels2 = list(dic.keys())


ping = db.execute('SELECT ping FROM ip')
for j, i in enumerate(ping):
    ping[j] = i[0]
ping = [a for a in ping if a is None]

y = list(range(1, len(ping)))

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Country",
        "Version",
        f'Ping (Avg: {int(sum(ping)/len(ping))})',
        "Plot 2"
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
    go.Bar(x=y, y=ping),
    row=2, col=1
)

fig.update_layout(title_text="SpaceInvador Statistics", template="plotly_dark")
fig.show()
