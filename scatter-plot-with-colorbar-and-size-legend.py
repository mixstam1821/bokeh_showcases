# my post: https://discourse.bokeh.org/t/scatter-plot-with-colorbar-and-size-legend/12531
from bokeh.palettes import Magma256
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, ColorBar, LinearColorMapper, CustomJSHover, HoverTool
from bokeh.layouts import row
import numpy as np
def cusj():
    num=1
    return CustomJSHover(code=f"""
    special_vars.indices = special_vars.indices.slice(0,{num})
    return special_vars.indices.includes(special_vars.index) ? " " : " hidden "
    """)
def hovfun(tltl):
    return """<div @hidden{custom} style="background-color: #fff0eb; padding: 5px; border-radius: 5px; box-shadow: 0px 0px 5px rgba(0,0,0,0.3);">        <font size="3" style="background-color: #fff0eb; padding: 5px; border-radius: 5px;"> """+tltl+""" <br> </font> </div> <style> :host { --tooltip-border: transparent;  /* Same border color used everywhere */ --tooltip-color: transparent; --tooltip-text: #2f2f2f;} </style> """
# Generate random data
np.random.seed(42)
x = np.random.rand(500) * 100  # X-coordinates
y = np.random.rand(500) * 100  # Y-coordinates
sizes = [10, 20, 30, 40] * 125
agreement_pc = np.random.rand(500) * 100 
# Create color mapper
color_mapper = LinearColorMapper(palette=Magma256, low=min(agreement_pc), high=max(agreement_pc))
colors = [Magma256[int((agr - min(agreement_pc)) / (max(agreement_pc) - min(agreement_pc)) * 255)] for agr in agreement_pc]

# Create data source
source = ColumnDataSource(data=dict(x=x, y=y, sizes=sizes, agreement_pc=agreement_pc, hidden=np.ones(len(x)) * np.min(y), colors=colors))

# Create a scatter plot
p = figure(title="Scatter Plot with Colorbar and Size Legend",
           x_axis_label="X-axis", y_axis_label="Y-axis",
           width=1350, height=800)

scatter = p.scatter('x', 'y', source=source, size='sizes', fill_color='colors', line_color=None, alpha=0.7, legend_label='', hover_line_color='black', hover_line_alpha=1, hover_line_width=3,hover_fill_color='colors')

# Add colorbar
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12, width=17, location=(0, 0),major_label_text_font_size='13pt')
p.add_layout(color_bar, 'right')
tltl = """<i>x:</i> <b>@x</b> <br> <i>y:</i> <b>@y</b><br> <i>size:</i> <b>@sizes</b><br> <i>agreement_pc:</i> <b>@agreement_pc</b>"""
p.add_tools(HoverTool(tooltips=hovfun(tltl), formatters={"@hidden": cusj()},mode="mouse",renderers = [scatter]))
p2 = figure(width=105, height=250, x_range=(-0.8,2), y_range=(-3,40),tools='',styles = {'margin-top': '300px','margin-left': '-110px'})
x_text = [0]*4
x2_text = [1.4]*4

y_text = [0, 10, 20, 30]
sizes = [10, 20, 30, 40]
text = ['0-10', '10-20', '20-30', '>30']
source_text = ColumnDataSource(data=dict(x=x_text,x2=x2_text, y=y_text, sizes=sizes, text=text))
p2.scatter('x', 'y', size='sizes', source=source_text, color='deepskyblue')
p2.text('x2', 'y', text='text', source=source_text, text_baseline="middle", text_align="center", text_font_size='12pt', text_color='deepskyblue')
p2.axis.visible = False
p2.grid.visible = False
p2.outline_line_color = None
p2.toolbar.logo = None
p2.toolbar_location = None
p.legend.visible=False
p.min_border_right = 180

laly = row(p,p2)
show(laly)
