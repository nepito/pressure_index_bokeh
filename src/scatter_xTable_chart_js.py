from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, ImageURL, LinearAxis
from bokeh.transform import jitter
from bokeh.layouts import row

url = "https://raw.githubusercontent.com/nepito/calculator-trs/develop/tests/data/logo_nies.png"

id_league = "61"
teams = pd.read_csv(f"/workdir/data/xTable_{id_league}_2022.csv")
teams["x"] = np.random.normal(1, 1, len(teams))

league_item = {
    "logo_url": f"https://media-3.api-sports.io/football/leagues/{id_league}.png",
    "min_x": teams["x"].min(),
    "max_x": teams["x"].max(),
    "min_p": teams["puntos"].min(),
    "min_xP": teams["xpuntos"].min(),
}


teams_records = teams.to_dict("records")

fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

rendered = env.get_template("xtable_chart_js.html").render(
    items=teams_records,
    league=league_item,
)
print(rendered)
