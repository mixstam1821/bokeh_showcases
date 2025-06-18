# see my post for more examples: https://discourse.bokeh.org/t/plot-on-hover-tooltip/12471
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.layouts import column

# 📦 Parameters
NUM_POINTS = 25
TIME_SERIES_LENGTH = 40

# 🎲 Generate fake station data
np.random.seed(1337)
x = np.random.rand(NUM_POINTS) * 100
y = np.random.rand(NUM_POINTS) * 100
station_ids = [f"Station {i}" for i in range(NUM_POINTS)]

# 📈 Generate timeseries PNG from matplotlib
def generate_timeseries_png(ts):
    fig, ax = plt.subplots(figsize=(2, 0.5), dpi=100)
    ax.plot(ts, color='#0072B2', linewidth=2)
    ax.set_axis_off()
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    return f"<img src='data:image/png;base64,{encoded}' width='150' height='40'/>"

# 🧠 Timeseries per station
station_series = {}
tooltips_png = []
for station in station_ids:
    ts = np.cumsum(np.random.randn(TIME_SERIES_LENGTH))
    station_series[station] = ts
    tooltips_png.append(generate_timeseries_png(ts))

# 📊 Data source
source = ColumnDataSource(data=dict(
    x=x,
    y=y,
    station=station_ids,
    png=tooltips_png
))

# 📈 Standard white Bokeh figure
p = figure(
    title="Scatter Plot with Matplotlib Tooltip Sparklines",
    width=800,
    height=600,
    tools="pan,wheel_zoom,reset,hover"
)

p.circle('x', 'y', size=10, source=source, color="#1f77b4", line_color="black", alpha=0.8)

# 🧠 Tooltip with base64 PNG
hover = p.select_one(HoverTool)
hover.tooltips = """
<div style="background-color:#f9f9f9; padding:6px; border-radius:5px; border:1px solid #ccc;">
  <div><strong>@station</strong></div>
  <div>@png{safe}</div>
</div>
"""

# 🚀 Launch app
curdoc().add_root(column(p))
