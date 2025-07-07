# https://discourse.bokeh.org/t/toolbar-button-to-change-the-chart-type/12501

from bokeh.plotting import figure, curdoc
from bokeh.models import (
    ColumnDataSource, HoverTool, CustomAction, CustomJS, FactorRange, Range1d
)
from bokeh.layouts import column
from datetime import datetime, timedelta

# -- Generate date strings for x-axis --
start_date = datetime(2024, 7, 1)
dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(12)]
values = [151,168,193,223,240,245,238,221,195,170,154,150]
source = ColumnDataSource(dict(x=dates, y=values))

factor_xrange = FactorRange(factors=dates)
factor_yrange = Range1d(start=min(values)*0.8, end=max(values)*1.1)

plot = figure(
    width=800, height=500, title='Bar/Line/Area Toggle (Datetime as String)',
    x_range=factor_xrange, y_range=factor_yrange, tools=[]
)

# Bar plot renderer
bar_renderer = plot.vbar(
    x='x', top='y', width=0.8, source=source,
    fill_color='#2596be', line_color='#18587c', alpha=0.85, name="bar"
)

# Line and scatter renderers
line_renderer = plot.line(
    x='x', y='y', source=source, line_width=3, color='#fb8c00', name="line"
)
circle_renderer = plot.circle(
    x='x', y='y', source=source, size=12, color='#d7263d', line_color='#333', name="scatter"
)
line_renderer.visible = False
circle_renderer.visible = False

# Area plot renderer
area_renderer = plot.varea(
    x='x', y1=0, y2='y', source=source, fill_color='#38a169', fill_alpha=0.45, name="area"
)
area_renderer.visible = False

# Tooltips
hover_bar = HoverTool(tooltips=[('Date', '@x'), ('Value', '@y')], renderers=[bar_renderer])
hover_point = HoverTool(tooltips=[('Date', '@x'), ('Value', '@y')], renderers=[circle_renderer])
hover_area = HoverTool(tooltips=[('Date', '@x'), ('Value', '@y')], renderers=[area_renderer])
plot.add_tools(hover_bar, hover_point, hover_area)

plot.xaxis.major_label_orientation = 0.7

plot.tags = [dates]  # For restoring x_range

# JS callback: cycle among bar, line+scatter, area
toggle_callback = CustomJS(
    args=dict(
        bar=bar_renderer,
        line=line_renderer,
        scatter=circle_renderer,
        area=area_renderer,
        plot=plot,
        factor_xrange=factor_xrange,
        factor_yrange=factor_yrange,
    ),
    code="""
    if (bar.visible) {
        bar.visible = false;
        line.visible = true;
        scatter.visible = true;
        area.visible = false;
        plot.title.text = "Line/Scatter Plot";
        plot.x_range = factor_xrange;
        plot.y_range = factor_yrange;
        plot.xaxis.visible = true;
        plot.yaxis.visible = true;
    } else if (line.visible) {
        bar.visible = false;
        line.visible = false;
        scatter.visible = false;
        area.visible = true;
        plot.title.text = "Area Plot";
        plot.x_range = factor_xrange;
        plot.y_range = factor_yrange;
        plot.xaxis.visible = true;
        plot.yaxis.visible = true;
    } else {
        bar.visible = true;
        line.visible = false;
        scatter.visible = false;
        area.visible = false;
        plot.title.text = "Bar Plot";
        plot.x_range = factor_xrange;
        plot.y_range = factor_yrange;
        plot.xaxis.visible = true;
        plot.yaxis.visible = true;
    }
    """
)

# Nice colored convert/transform icon SVG (arrows in a circle)
svg_icon = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" fill="#e0f2fe" stroke="#2596be" stroke-width="2"/>
  <path d="M7 12l-2-2 2-2" stroke="#fb8c00" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M17 12l2 2-2 2" stroke="#38a169" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M5 10h7a2 2 0 012 2v4" stroke="#18587c" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M19 14h-7a2 2 0 01-2-2V8" stroke="#d7263d" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

toggle_action = CustomAction(
    icon=f"data:image/svg+xml;base64,{svg_icon.encode('utf-8').hex()}",
    description="Toggle Bar/Line/Area",
    callback=toggle_callback
)

import base64
toggle_action.icon = "data:image/svg+xml;base64," + base64.b64encode(svg_icon.encode('utf-8')).decode()

plot.add_tools(toggle_action)

curdoc().add_root(column(plot))
curdoc().title = "Bar <-> Line <-> Area Toggle"









# STATIC
from bokeh.plotting import figure, output_file, save
from bokeh.models import (
    ColumnDataSource, HoverTool, CustomAction, CustomJS, FactorRange, Range1d
)
from datetime import datetime, timedelta
import base64

# Generate date strings for x-axis
start_date = datetime(2024, 7, 1)
dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(12)]
values = [151,168,193,223,240,245,238,221,195,170,154,150]
source = ColumnDataSource(dict(x=dates, y=values))

factor_xrange = FactorRange(factors=dates)
factor_yrange = Range1d(start=min(values)*0.8, end=max(values)*1.1)

plot = figure(
    width=800, height=500, title='Bar/Line/Area Toggle (Datetime as String)',
    x_range=factor_xrange, y_range=factor_yrange, tools=[]
)

# Renderers
bar_renderer = plot.vbar(
    x='x', top='y', width=0.8, source=source,
    fill_color='#2596be', line_color='#18587c', alpha=0.85, name="bar"
)
line_renderer = plot.line(
    x='x', y='y', source=source, line_width=3, color='#fb8c00', name="line"
)
circle_renderer = plot.circle(
    x='x', y='y', source=source, size=12, color='#d7263d', line_color='#333', name="scatter"
)
area_renderer = plot.varea(
    x='x', y1=0, y2='y', source=source, fill_color='#38a169', fill_alpha=0.45, name="area"
)
line_renderer.visible = False
circle_renderer.visible = False
area_renderer.visible = False

plot.xaxis.major_label_orientation = 0.7

# --- Only ONE hover tool, dynamically switched ---
hover = HoverTool(
    tooltips=[('Date', '@x'), ('Value', '@y')],
    renderers=[bar_renderer],
    name="universal_hover"
)
plot.add_tools(hover)
plot.toolbar.active_inspect = [hover]

# JS callback: dynamically update hover for the active plot type
toggle_callback = CustomJS(
    args=dict(
        bar=bar_renderer,
        line=line_renderer,
        scatter=circle_renderer,
        area=area_renderer,
        plot=plot,
        hover=hover,
        factor_xrange=factor_xrange,
        factor_yrange=factor_yrange,
    ),
    code="""
    if (bar.visible) {
        bar.visible = false;
        line.visible = true;
        scatter.visible = true;
        area.visible = false;
        plot.title.text = "Line/Scatter Plot";
        hover.renderers = [scatter];
        hover.tooltips = [['Date', '@x'], ['Value', '@y']];
        plot.toolbar.active_inspect = [hover];
    } else if (line.visible) {
        bar.visible = false;
        line.visible = false;
        scatter.visible = false;
        area.visible = true;
        plot.title.text = "Area Plot";
        hover.renderers = [area];
        hover.tooltips = [['Date', '@x'], ['Value', '@y']];
        plot.toolbar.active_inspect = [hover];
    } else {
        bar.visible = true;
        line.visible = false;
        scatter.visible = false;
        area.visible = false;
        plot.title.text = "Bar Plot";
        hover.renderers = [bar];
        hover.tooltips = [['Date', '@x'], ['Value', '@y']];
        plot.toolbar.active_inspect = [hover];
    }
    """
)

# Nice colored convert/transform icon SVG (arrows in a circle)
svg_icon = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" fill="#e0f2fe" stroke="#2596be" stroke-width="2"/>
  <path d="M7 12l-2-2 2-2" stroke="#fb8c00" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M17 12l2 2-2 2" stroke="#38a169" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M5 10h7a2 2 0 012 2v4" stroke="#18587c" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M19 14h-7a2 2 0 01-2-2V8" stroke="#d7263d" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

toggle_action = CustomAction(
    icon=f"data:image/svg+xml;base64,{svg_icon.encode('utf-8').hex()}",
    description="Toggle Bar/Line/Area",
    callback=toggle_callback
)

import base64
toggle_action.icon = "data:image/svg+xml;base64," + base64.b64encode(svg_icon.encode('utf-8')).decode()

plot.add_tools(toggle_action)

output_file("bokeh_toggle_plot.html")
save(plot)
