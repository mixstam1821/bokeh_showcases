# see my post here: https://discourse.bokeh.org/t/animated-waves/12429

# Amphitrite.py
import numpy as np

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

# ─── PARAMETERS ────────────────────────────────────────────────────────────────
N_POINTS           = 1000    # super-smooth curves
WIDTH              = 10.0
UPDATE_INTERVAL_MS = 20      # ~50 fps

# each layer: amplitude, vertical offset, frequency (cycles/sec), color, alpha
LAYERS = [
    {"ampl": 0.6, "offset": -0.3, "freq": 0.4, "color": "#007acc", "alpha": 0.8},
    {"ampl": 0.5, "offset":  0.0, "freq": 0.6, "color": "#005f9e", "alpha": 0.7},
    {"ampl": 0.4, "offset":  0.4, "freq": 0.8, "color": "#00ddff", "alpha": 0.6},
]

# x axis
x = np.linspace(0, WIDTH, N_POINTS)

# ─── FIGURE SETUP ───────────────────────────────────────────────────────────────
p = figure(
    x_range=(0, WIDTH),
    y_range=(-2, 2.5),
    sizing_mode="stretch_both",
    tools="",
)

# hide axes, grids, borders, background
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.background_fill_color = None
p.border_fill_color     = None
p.min_border_left = p.min_border_right = p.min_border_top = p.min_border_bottom = 0

# ─── BACKGROUND IMAGE ───────────────────────────────────────────────────────────
# a Santorini sunset photo 
image_url = "https://images.unsplash.com/photo-1731188355505-f0e9277879dd?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGdyZWVjZSUyMHN1bnNldHxlbnwwfHwwfHx8MA%3D%3D"
# cover the whole plot area (x:0→10, y:-2→2.5 => height ≈4.5)
p.image_url(
    url=[image_url],
    x=0, y=2.5,      # y=top of image
    w=WIDTH, h=4.5,
    anchor="top_left",
    global_alpha=1.0
)


from bokeh.models import Label

label = Label(
    x=WIDTH/2, y=-1.1,                   # data-space coords at the top
    x_units='data', y_units='data',
    text='Bokeh Rocks',
    text_align='center',
    text_font_size='44px',
    text_font_style='bold italic',
    text_color='white',
    text_font='Georgia', 
)
p.add_layout(label)

# ─── WAVE LAYERS ────────────────────────────────────────────────────────────────
sources = []
for layer in LAYERS:
    y1 = layer["offset"] + layer["ampl"] * np.sin(2*np.pi*(x/WIDTH*2))
    y2 = np.full_like(x, -2)
    src = ColumnDataSource(data=dict(x=x, y1=y1, y2=y2))
    p.varea("x", "y1", "y2", source=src,
            fill_color=layer["color"], fill_alpha=layer["alpha"])
    sources.append(src)

# track each layer's phase
phases = np.zeros(len(LAYERS))

def update():
    dt = UPDATE_INTERVAL_MS / 1000.0
    for i, (layer, src) in enumerate(zip(LAYERS, sources)):
        phases[i] += layer["freq"] * dt
        y1 = layer["offset"] + layer["ampl"] * np.sin(
            2*np.pi*(x/WIDTH*2 + phases[i])
        )
        src.data = dict(x=x, y1=y1, y2=np.full_like(x, -2))

# hook it up
curdoc().add_root(p)
curdoc().add_periodic_callback(update, UPDATE_INTERVAL_MS)
