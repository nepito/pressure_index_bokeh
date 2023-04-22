from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, ImageURL, HoverTool

url = "https://raw.githubusercontent.com/nepito/calculator-trs/develop/tests/data/logo_nies.png"


def assing_color(x):
    if x < 6:
        return "blue"
    if x > 17:
        return "red"
    return "orange"


bdp_and_ppda = pd.read_csv("/workdir/data/pression_index_39_2022.csv")
bdp_and_ppda["color"] = bdp_and_ppda["premier"].map(assing_color)
source = ColumnDataSource(data=bdp_and_ppda)

TOOLTIPS = [
    ("Equipo", "@{team}"),
    ("Premier", "@{premier}"),
]

p = figure(
    title="PPDA vs BDP de la Premier League en el año 2022-2023",
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

r1 = p.circle(x="build_up_disruption", y="ppda", size=8, source=source, color="color")
width = 1
height = 1.8
image3 = ImageURL(url=dict(value=url), x=-3.2, y=6, h=height, w=width, anchor="bottom_left")
p.add_glyph(source, image3)
p.xaxis.axis_label = "Build-up disruption"
p.yaxis.axis_label = "PPDA"
p.line(x, y_predicted, color="black")
hover = HoverTool(renderers=[r1], tooltips=TOOLTIPS)
p.add_tools(hover)
script, div = components(p)
fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

rendered = env.get_template("bdp_vs_ppda.html").render(
    script=script,
    div=div,
)
print(rendered)
