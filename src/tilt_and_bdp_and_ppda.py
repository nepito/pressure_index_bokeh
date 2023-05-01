from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, ImageURL, HoverTool, Span
import json

# JSON file
league = "135"
summary_path = f"/workdir/results/summary_tilt_bdp_ppda_{league}.json"
f = open(summary_path, "r")
# Reading from file
summary_tilt_bdp_ppda = json.loads(f.read())

url = "https://raw.githubusercontent.com/nepito/calculator-trs/develop/tests/data/logo_nies.png"


def assing_color_serie_a(x):
    if x < 7:
        return "blue"
    if x > 17:
        return "red"
    return "orange"


def assing_future_serie_a(x):
    if x < 7:
        return "Zona europea"
    if x > 17:
        return "Descenso"
    return "Sin novedad"


def assing_color_premier(x):
    if x < 6:
        return "blue"
    if x > 17:
        return "red"
    return "orange"


def assing_color_mx(x):
    if x < 5:
        return "blue"
    if x > 12:
        return "red"
    return "orange"


assing_color = {
    "262": assing_color_mx,
    "39": assing_color_premier,
    "263": assing_color_mx,
    "135": assing_color_serie_a,
}

bdp_and_ppda = pd.read_csv(f"/workdir/data/pression_index_{league}_2022.csv").sort_values(
    by=["tilt"], ascending=False
)
bdp_and_ppda["color"] = bdp_and_ppda["league"].map(assing_color[league])
bdp_and_ppda["futuro"] = bdp_and_ppda["league"].map(assing_future_serie_a)
source = ColumnDataSource(data=bdp_and_ppda)

TOOLTIPS = [
    ("Equipo", "@{team}"),
    ("Posición", "@{league}"),
    ("xG", "@{xG}"),
]
name_league = {
    "262": "Liga MX",
    "263": "Liga de Expansión MX",
    "39": "Premier League",
    "135": "Serie A",
}
p = figure(
    title=f"PPDA vs BDP \n{name_league[league]} en el año 2022-2023",
    toolbar_location=None,
    sizing_mode="scale_both",
    aspect_ratio=2,
)

x = np.array(bdp_and_ppda["build_up_disruption"])
y = np.array(bdp_and_ppda["ppda"])
par = np.polyfit(x, y, 1, full=True)
slope = par[0][0]
intercept = par[0][1]
y_predicted = [slope * i + intercept for i in x]

r1 = p.circle(
    x="build_up_disruption", y="ppda", size=8, source=source, color="color", legend="futuro",
)
width = 1
height = 1.0
image3 = ImageURL(url=dict(value=url), x=-2, y=8, h=height, w=width, anchor="bottom_left")
p.add_glyph(source, image3)
p.xaxis.axis_label = "Build-up disruption"
p.yaxis.axis_label = "PPDA"
p.line(x, y_predicted, color="black")
hover = HoverTool(renderers=[r1], tooltips=TOOLTIPS)
p.add_tools(hover)

script, div = components(p)
items = bdp_and_ppda.to_dict("records")
#%%%             Esta es la sección
arsenal = pd.read_csv("/workdir/data/napoli_serie_a.csv")
arsenal["Date"] = pd.to_datetime(arsenal["Date"])
source = ColumnDataSource(data=arsenal)

leader_team = "Napoli"
TOOLTIPS = [
    ("Partido", "@{Match}"),
    (f"Inclinación {leader_team}", "@{tilt}"),
    ("Inclinación Rival", "@{rivales}"),
]

p = figure(
    title=f"Inclinación del {leader_team} en el año 2022-2023",
    toolbar_location=None,
    tools="hover",
    tooltips=TOOLTIPS,
    x_axis_type="datetime",
    sizing_mode="scale_both",
    aspect_ratio=2,
    x_range=(
        arsenal["Date"].iloc[-1] - pd.DateOffset(days=10),
        arsenal["Date"].iloc[0] + pd.DateOffset(days=10),
    ),
)

tilt_mean = bdp_and_ppda["tilt"].mean()
tilt_std = bdp_and_ppda["tilt"].std()
p.circle(x="Date", y="tilt", size=8, source=source)
hline_sup = Span(
    location=tilt_mean + tilt_std,
    dimension="width",
    line_color="green",
    line_width=2,
    line_dash="dashed",
)
hline_inf = Span(
    location=tilt_mean - tilt_std,
    dimension="width",
    line_color="red",
    line_width=2,
    line_dash="dashed",
)
width = arsenal["Date"].iloc[0] - arsenal["Date"].iloc[9]
height = 10
image3 = ImageURL(
    url=dict(value=url),
    x=arsenal["Date"].iloc[-1],
    y=24,
    h=height,
    w=width,
    anchor="bottom_left",
)
p.add_glyph(source, image3)
p.xaxis.axis_label = ""
p.yaxis.axis_label = "Inclinación del juego (%)"
p.renderers.extend([hline_sup, hline_inf])
script_tilt, div_tilt = components(p)
# %%%
fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

rendered = env.get_template("tilt_and_bdp_vs_ppda.html").render(
    script=script,
    div=div,
    script_t=script_tilt,
    div_t=div_tilt,
    items=items,
    summary=summary_tilt_bdp_ppda,
    league=name_league[league],
)
print(rendered)
