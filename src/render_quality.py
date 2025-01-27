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

bdp_and_ppda = pd.read_csv(f"/workdir/quality_and_pression_index.csv").sort_values(
    by=["tilt"], ascending=False
)
bdp_and_ppda["color"] = bdp_and_ppda["idx"].map(assing_color[league])
bdp_and_ppda["futuro"] = bdp_and_ppda["idx"].map(assing_future_serie_a)
source = ColumnDataSource(data=bdp_and_ppda)

TOOLTIPS = [
    ("Equipo", "@{name}"),
    ("Posición", "@{idx}"),
    ("xG", "@{xG}"),
]
name_league = {
    "262": "Liga MX",
    "263": "Liga de Expansión MX",
    "39": "Premier League",
    "135": "Serie A",
}
p = figure(
    title=f"PPDA vs BDP \n{name_league[league]} en el año 2023-2024",
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
    x="build_up_disruption",
    y="ppda",
    size=8,
    source=source,
    color="color",
    legend="futuro",
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
leader_team = "Inter"
# %%%
fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

rendered = env.get_template("quality_template.jinja").render(
    script=script,
    div=div,
    items=items,
    summary=summary_tilt_bdp_ppda,
    league=name_league[league],
    leader_team = leader_team,
)
print(rendered)
