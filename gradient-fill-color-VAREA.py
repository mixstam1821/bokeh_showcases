# my post: https://discourse.bokeh.org/t/gradient-fill-color/12252/7

from bokeh.plotting import figure, show
from bokeh.models import InlineStyleSheet
from bokeh.layouts import column
import numpy as np

# Generate sample data
x = np.linspace(0, 4 * np.pi, 100)
y = np.sin(x) * 2 - 1 

# Create figure
p = figure(
    width=800,
    height=600,
    title="Gradient Background with Line Masking",
    x_axis_label="X",
    y_axis_label="Y",
    y_range=(y.min()-np.abs(y.min())/2, y.max()+np.abs(y.max())/2),  # Set fixed y range
    x_range=(x.min(), x.max())
)

max_y = y.max()*100
p.varea(
    x=x,
    y1=y,        # Bottom of mask = the line
    y2=max_y,    # Top of mask = top of plot
    fill_color='tan',
    fill_alpha=1,
)

# make tan before the x.min
p.varea(
    x=np.linspace(-100, 0, 100),
    y1=-max_y,       
    y2=max_y,    
    fill_color='tan',
    fill_alpha=1,
)

# make tan after the x.max
p.varea(
    x=np.linspace(4 * np.pi, 100, 100),
    y1=-max_y,       
    y2=max_y,    
    fill_color='tan',
    fill_alpha=1,
)

# Step 3: Draw the line on top (this creates the "border" between areas)
p.line(
    x=x,
    y=y,
    line_color='black',
    line_width=3,
    line_alpha=1.0
)

# Styling
p.background_fill_color = None    
p.border_fill_color = "white"         
p.outline_line_color = "#cccccc"
p.grid.grid_line_color = None
p.grid.grid_line_alpha = 0
p.title.text_font_size = "16pt"
p.title.text_color = "#2c3e50"

gradient_css = InlineStyleSheet(css="""
:host {
background: linear-gradient(to bottom, #1de9b6 0%, #b2ff59 50%, #ffd600 100%);
}
""")
show(column(p, stylesheets=[gradient_css]))











from bokeh.plotting import figure, show
from bokeh.models import InlineStyleSheet, ColumnDataSource, HoverTool
from bokeh.layouts import row, column
import numpy as np

def make_neon_plot(gradient_css, title):
    x = np.linspace(0, 4 * np.pi, 100)
    y = np.sin(x) * 2 - 1 
    source = ColumnDataSource(data=dict(x=x, y=y))
    max_y = y.max()*100
    dark_mask = "#181843"

    p = figure(
        width=500,
        height=400,
        title=title,
        x_axis_label="X",
        y_axis_label="Y",
        y_range=(y.min()-np.abs(y.min())/2, y.max()+np.abs(y.max())/2),
        x_range=(x.min(), x.max())
    )

    # varea: under the curve (to top)
    p.varea(
        x=x,
        y1=y,
        y2=max_y,
        fill_color=dark_mask,
        fill_alpha=0.98,
    )
    # varea: before left, after right
    p.varea(
        x=np.linspace(-100, 0, 100),
        y1=-max_y,       
        y2=max_y,    
        fill_color=dark_mask,
        fill_alpha=0.98,
    )
    p.varea(
        x=np.linspace(4 * np.pi, 100, 100),
        y1=-max_y,       
        y2=max_y,    
        fill_color=dark_mask,
        fill_alpha=0.98,
    )

    # Neon line (cyan)
    p.line(
        x='x',
        y='y',
        source=source,
        line_color="#03e9f4",  # Neon cyan
        line_width=4,
        line_alpha=1.0,
        name="main_line"
    )

    hover = HoverTool(
        tooltips=[
            ("X", "@x{0.00}"),
            ("Y", "@y{0.00}")
        ],
        mode='vline',
        renderers=[p.select(name="main_line")[0]]
    )
    p.add_tools(hover)

    # Styling
    p.background_fill_color = None
    p.border_fill_color = "#0b0824"
    p.outline_line_color = "#181843"
    p.grid.grid_line_color = "#282872"
    p.grid.grid_line_alpha = 0.12
    p.title.text_font_size = "15pt"
    p.title.text_color = "#f500ea"
    p.xaxis.axis_label_text_color = "#1de9b6"
    p.yaxis.axis_label_text_color = "#1de9b6"
    p.xaxis.major_label_text_color = "#b2ff59"
    p.yaxis.major_label_text_color = "#b2ff59"

    return p, InlineStyleSheet(css=gradient_css)

# Neon gradients
vertical_css = """
:host {
  background: linear-gradient(to bottom,
    #22223b 0%,
    #383ba8 40%,
    #7b2ff2 55%,
    #f357a8 75%,
    #03e9f4 100%);
}
"""

horizontal_css = """
:host {
  background: linear-gradient(to right,
    #22223b 0%,
    #383ba8 40%,
    #7b2ff2 55%,
    #f357a8 75%,
    #03e9f4 100%);
}
"""

diagonal_css = """
:host {
  background: linear-gradient(45deg,
    #22223b 0%,
    #383ba8 40%,
    #7b2ff2 55%,
    #f357a8 75%,
    #03e9f4 100%);
}
"""

p1, css1 = make_neon_plot(vertical_css, "Top-to-Bottom Neon Gradient")
p2, css2 = make_neon_plot(horizontal_css, "Left-to-Right Neon Gradient")
p3, css3 = make_neon_plot(diagonal_css, "45° Angle Neon Gradient")

show(row(
    column(p1, stylesheets=[css1]),
    column(p2, stylesheets=[css2]),
    column(p3, stylesheets=[css3])
))














from bokeh.plotting import figure, show
from bokeh.models import InlineStyleSheet, ColumnDataSource, HoverTool
from bokeh.layouts import row, column
import numpy as np

def make_fancy_light_plot(gradient_css, title):
    x = np.linspace(0, 4 * np.pi, 100)
    y = np.sin(x) * 2 - 1 
    source = ColumnDataSource(data=dict(x=x, y=y))
    max_y = y.max()*100
    pastel_mask = "#fff3e0"  # Light pastel orange/peach

    p = figure(
        width=500,
        height=400,
        title=title,
        x_axis_label="X",
        y_axis_label="Y",
        y_range=(y.min()-np.abs(y.min())/2, y.max()+np.abs(y.max())/2),
        x_range=(x.min(), x.max())
    )

    # Mask area: pastel for contrast, not too dark
    p.varea(
        x=x,
        y1=y,
        y2=max_y,
        fill_color=pastel_mask,
        fill_alpha=0.95,
    )
    p.varea(
        x=np.linspace(-100, 0, 100),
        y1=-max_y,       
        y2=max_y,    
        fill_color=pastel_mask,
        fill_alpha=0.95,
    )
    p.varea(
        x=np.linspace(4 * np.pi, 100, 100),
        y1=-max_y,       
        y2=max_y,    
        fill_color=pastel_mask,
        fill_alpha=0.95,
    )

    # Bright line: electric blue/violet for eye-catching contrast
    p.line(
        x='x',
        y='y',
        source=source,
        line_color="#5f2eea",  # Vibrant violet
        line_width=4,
        line_alpha=1.0,
        name="main_line"
    )

    hover = HoverTool(
        tooltips=[
            ("X", "@x{0.00}"),
            ("Y", "@y{0.00}")
        ],
        mode='vline',
        renderers=[p.select(name="main_line")[0]]
    )
    p.add_tools(hover)

    # Fancy light theme styling
    p.background_fill_color = None
    p.border_fill_color = "#fffde7"   # Light yellow
    p.outline_line_color = "#ffe082"
    p.grid.grid_line_color = "#ffb74d"
    p.grid.grid_line_alpha = 0.17
    p.title.text_font_size = "15pt"
    p.title.text_color = "#ea4c89"    # Fancy pink
    p.xaxis.axis_label_text_color = "#00c9b7"  # Aqua
    p.yaxis.axis_label_text_color = "#00c9b7"
    p.xaxis.major_label_text_color = "#fe8c00"  # Orange
    p.yaxis.major_label_text_color = "#fe8c00"

    return p, InlineStyleSheet(css=gradient_css)

# Fancy light gradients
vertical_css = """
:host {
  background: linear-gradient(to bottom,
    #fffde7 0%,
    #ffe082 25%,
    #ffb74d 55%,
    #fcb69f 75%,
    #a1c4fd 100%);
}
"""

horizontal_css = """
:host {
  background: linear-gradient(to right,
    #fffde7 0%,
    #ffe082 25%,
    #ffb74d 55%,
    #eaafc8 75%,
    #d4fc79 100%);
}
"""

diagonal_css = """
:host {
  background: linear-gradient(45deg,
    #fffde7 0%,
    #b2fefa 30%,
    #fcb69f 55%,
    #fdc094 75%,
    #eaafc8 100%);
}
"""

p1, css1 = make_fancy_light_plot(vertical_css, "Top-to-Bottom Fancy Gradient")
p2, css2 = make_fancy_light_plot(horizontal_css, "Left-to-Right Fancy Gradient")
p3, css3 = make_fancy_light_plot(diagonal_css, "45° Angle Fancy Gradient")

show(row(
    column(p1, stylesheets=[css1]),
    column(p2, stylesheets=[css2]),
    column(p3, stylesheets=[css3])
))
