# https://discourse.bokeh.org/t/interactive-trend-line-as-option-in-toolbar/12485
import numpy as np
import pandas as pd
import datetime
from bokeh.plotting import figure, curdoc
from bokeh.models import PointDrawTool, ColumnDataSource, HoverTool, Div, CustomAction, CustomJS
from scipy.stats import linregress, theilslopes
from bokeh.layouts import column

# ---- Frequency options ----
# Uncomment the freq you want to test

#freq = 'Y'   # yearly
freq = 'M'   # monthly
#freq = 'D'   # daily
#freq = 'H'   # hourly
#freq = 'T'   # minutely
# freq = 'S'    # secondly

N = 30
x_pd = pd.date_range("2020-01-01", periods=N, freq=freq)
x = x_pd.to_pydatetime()
y = np.cumsum(np.random.randn(N)) + 10  # random walk

# ---- Main plot ----
p = figure(width=800, height=500, title='Interactive Slope, OLS & Theil–Sen', x_axis_type="datetime")
p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Value'
main_line = p.line(x, y, line_width=2, color="#08f", legend_label="Time Series")
p.circle(x, y, size=7, color="#08f", alpha=0.7)

# ---- Trend line for user selection ----
trend_source = ColumnDataSource(data={'x': [x[5], x[20]], 'y': [y[5], y[20]]})
trend_points = p.scatter(x='x', y='y', size=10, fill_color='orange', line_color='black', source=trend_source)
trend_line = p.line(x='x', y='y', line_color='orange', line_width=3, source=trend_source)
trend_points.visible = False
trend_line.visible = False

draw_tool = PointDrawTool(renderers=[trend_points], add=False)
p.add_tools(draw_tool)
p.add_tools(HoverTool(tooltips=[('Time', '@x{%F %T}'), ('Value', '@y')],
                      formatters={'@x': 'datetime'}, renderers=[main_line]))

results_div = Div(text="<b>Interactive mode disabled. Click the toggle tool in toolbar to start analysis.</b>", 
                  width=1100, styles={'color': 'black', 'background-color': 'lightgray', 'padding':'8px', 'border-radius':'8px'})

# ---- JavaScript toggle ----
toggle_callback = CustomJS(
    args=dict(
        trend_points=trend_points,
        trend_line=trend_line,
        draw_tool=draw_tool,
        results_div=results_div,
        plot=p
    ),
    code="""
    // Toggle visibility
    const currently_visible = trend_points.visible;
    trend_points.visible = !currently_visible;
    trend_line.visible = !currently_visible;
    if (!currently_visible) {
        plot.toolbar.active_tap = draw_tool;
        results_div.text = "<b>Interactive mode enabled! Drag the red endpoints to analyze different segments.</b>";
    } else {
        plot.toolbar.active_tap = null;
        results_div.text = "<b>Interactive mode disabled. Click the toggle tool in toolbar to start analysis.</b>";
    }
    """
)
toggle_action = CustomAction(
    icon="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cGF0aCBkPSJNNCAyMEwyMCA0IiBzdHJva2U9IiNmZjY2MDAiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+Cjwvc3ZnPgo=",
    description="Toggle Interactive Mode",
    callback=toggle_callback
)
p.add_tools(toggle_action)

# ---- Helper: handle all types for Bokeh JS datetime ----
def ensure_datetime(val):
    if isinstance(val, datetime.datetime):
        return val
    elif isinstance(val, (float, int)):
        return datetime.datetime.utcfromtimestamp(val / 1000.0)
    elif isinstance(val, str):
        try:
            return datetime.datetime.fromisoformat(val)
        except Exception:
            pass
    raise ValueError(f"Cannot convert {val} to datetime")

def closest_idx(dt, x_array):
    dt = ensure_datetime(dt)
    return np.argmin([abs((xi - dt).total_seconds()) for xi in x_array])

def pretty_timedelta(dt1, dt0):
    """
    Returns (value, unit) tuple for delta between two datetimes,
    with support for years, months, days, hours, minutes, seconds.
    """
    delta = dt1 - dt0
    total_seconds = abs(delta.total_seconds())
    total_days = total_seconds / (24*3600)

    # Years
    if total_days >= 730:
        years = abs(dt1.year - dt0.year)
        # Adjust for whether we've passed the month/day mark
        if dt1.month < dt0.month or (dt1.month == dt0.month and dt1.day < dt0.day):
            years -= 1
        years = max(years, 1)
        return (total_days / 365.25, "years")
    # Months
    elif total_days >= 60:
        # Count months between two dates
        months = abs((dt1.year - dt0.year) * 12 + (dt1.month - dt0.month))
        if dt1.day < dt0.day:
            months -= 1
        months = max(months, 1)
        return (total_days / 30.44, "months")
    elif total_days >= 2:
        return (total_days, "days")
    elif total_seconds >= 3600:
        return (total_seconds / 3600, "hours")
    elif total_seconds >= 60:
        return (total_seconds / 60, "minutes")
    else:
        return (total_seconds, "seconds")


def update_div(attr, old, new):
    xs = trend_source.data['x']
    ys = trend_source.data['y']
    if len(xs) != 2 or len(ys) != 2:
        results_div.text = "<b>Drag endpoints. Slope, OLS, Theil–Sen will show here.</b>"
        return

    dt0 = ensure_datetime(xs[0])
    dt1 = ensure_datetime(xs[1])

    idx0 = closest_idx(dt0, x)
    idx1 = closest_idx(dt1, x)

    if idx0 == idx1 or not (0 <= idx0 < N and 0 <= idx1 < N):
        results_div.text = "<b>Select two <i>different</i> points within range.</b>"
        return

    lo, hi = sorted([idx0, idx1])
    x_sel = x[lo:hi+1]
    y_sel = y[lo:hi+1]
    if len(x_sel) > 1:
        ols = linregress(np.arange(lo, hi+1), y_sel).slope
        ols_pv = linregress(np.arange(lo, hi+1), y_sel).pvalue
        theil = theilslopes(y_sel, np.arange(lo, hi+1))[0]
    else:
        ols = np.nan
        theil = np.nan

    delta_val, delta_unit = pretty_timedelta(dt1, dt0)
    dy = ys[1] - ys[0]
    slope = dy / delta_val if delta_val != 0 else float('nan')
    slope_str = f"Slope = {slope:.3f} per {delta_unit[:-1]}" if delta_val != 0 else "Slope = ∞"
    results_div.text = (
        f"<b>x0 = {dt0.strftime('%Y-%m-%d %H:%M:%S')}, y0 = {ys[0]:.2f},<br>"
        f"x1 = {dt1.strftime('%Y-%m-%d %H:%M:%S')}, y1 = {ys[1]:.2f},<br>"
        f"Δx = {delta_val:.3f} {delta_unit[:-1]}, Δy = {dy:.2f}, {slope_str}<br>"
        f"OLS Slope = {ols:.3f}, OLS p-value = {ols_pv:.5f}, Theil–Sen Slope = {theil:.3f}</b>"
    )

trend_source.on_change('data', update_div)

curdoc().add_root(column(p, results_div))
curdoc().title = f"Interactive Timeseries Slope: {freq}ly data"







# STATIC

import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import PointDrawTool, ColumnDataSource, HoverTool, Div, CustomAction, CustomJS
from bokeh.layouts import column

# Generate random time series data
np.random.seed(0)
N = 30
x = np.arange(N)
y = np.cumsum(np.random.randn(N)) + 10  # random walk

p = figure(width=800, height=500, title='Interactive Δx, Δy, Slope')
p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Value'
main_line = p.line(x, y, line_width=2, color="#08f")
p.circle(x, y, size=7, color="#08f", alpha=0.7)

trend_source = ColumnDataSource(data={'x': [5, 20], 'y': [y[5], y[20]]})
trend_points = p.scatter(x='x', y='y', size=10, fill_color='orange', line_color='black', source=trend_source)
trend_line = p.line(x='x', y='y', line_color='orange', line_width=3, source=trend_source)

trend_points.visible = False
trend_line.visible = False

draw_tool = PointDrawTool(renderers=[trend_points], add=False)
p.add_tools(draw_tool)
p.add_tools(HoverTool(tooltips=[('Time', '$x'), ('Value', '$y')], renderers=[main_line]))

results_div = Div(
    text="<b>Interactive mode disabled. Click the toggle tool in toolbar to start analysis.</b>",
    width=800, styles={'color': 'black', 'background-color': 'lightgray', 'padding': '8px', 'border-radius': '8px'}
)

# --- JS callback for updating results_div with dx, dy, slope ---
update_callback = CustomJS(
    args=dict(
        trend_source=trend_source,
        results_div=results_div
    ),
    code="""
    const xs = trend_source.data.x, ys = trend_source.data.y;
    if (xs.length != 2 || ys.length != 2) {
        results_div.text = "<b>Drag endpoints. Slope will show here.</b>";
        return;
    }
    let x0 = xs[0], x1 = xs[1], y0 = ys[0], y1 = ys[1];
    let dx = x1 - x0, dy = y1 - y0;
    let slope_str;
    if (dx != 0) {
        let slope = dy / dx;
        slope_str = "Slope = " + slope.toFixed(3);
    } else {
        slope_str = "Slope = ∞";
    }
    results_div.text = `<b>Δx = ${dx.toFixed(2)}, Δy = ${dy.toFixed(2)}, ${slope_str}</b>`;
    """
)
trend_source.js_on_change('data', update_callback)

# --- Toolbar toggle button for interactive mode ---
toggle_callback = CustomJS(
    args=dict(
        trend_points=trend_points,
        trend_line=trend_line,
        draw_tool=draw_tool,
        results_div=results_div,
        plot=p
    ),
    code="""
    const currently_visible = trend_points.visible;
    trend_points.visible = !currently_visible;
    trend_line.visible = !currently_visible;
    if (!currently_visible) {
        plot.toolbar.active_tap = draw_tool;
        results_div.text = "<b>Interactive mode enabled! Drag the orange endpoints to analyze.</b>";
    } else {
        plot.toolbar.active_tap = null;
        results_div.text = "<b>Interactive mode disabled. Click the toggle tool in toolbar to start analysis.</b>";
    }
    """
)
toggle_action = CustomAction(
    icon="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cGF0aCBkPSJNNCAyMEwyMCA0IiBzdHJva2U9IiNmZjY2MDAiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+Cjwvc3ZnPgo=",
    description="Toggle Interactive Mode",
    callback=toggle_callback
)
p.add_tools(toggle_action)

output_file("minimal_slope_interactive.html")
show(column(p, results_div))
