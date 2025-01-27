# see also here my post: https://discourse.bokeh.org/t/custom-animated-image-url-weather-symbols/12261

from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import ColorBar, BasicTicker, LinearColorMapper, ColumnDataSource, Button
from bokeh.models import WMTSTileSource
import numpy as np
import xyzservices.providers as xyz

def to_web_mercator(lon, lat):
    r = 6378137
    x = lon * (r * np.pi/180)
    y = np.log(np.tan((90 + lat) * np.pi/360)) * r
    return x, y

# Create the figure
p = figure(width=1200, height=600, x_axis_type="mercator", y_axis_type="mercator")

p.add_tile(xyz.CartoDB.DarkMatter, retina=True)
# Remove grid lines
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.xaxis.axis_line_color = None
p.yaxis.axis_line_color = None
# Set up coordinates for Europe region
europe_lon, europe_lat = 15, 40
x_europe, y_europe = to_web_mercator(europe_lon, europe_lat)


north_lon, north_lat = 30, 50
x_north, y_north = to_web_mercator(north_lon, north_lat)

africa_lon, africa_lat = 15, 20
x_africa, y_africa = to_web_mercator(africa_lon, africa_lat)


# Parameters for rain
num_raindrops = 20
x_spread = 2000000
y_height = 1000000
fall_speed = 15000

# Initialize random positions for raindrops
x_positions = [x_europe + np.random.uniform(-x_spread/2, x_spread/2) for _ in range(num_raindrops)]
y_positions = [y_europe + y_height + np.random.uniform(0, y_height) for _ in range(num_raindrops)]


x_positions2 = [x_north + np.random.uniform(-x_spread/2, x_spread/2) for _ in range(num_raindrops)]
y_positions2 = [y_north + y_height + np.random.uniform(0, y_height) for _ in range(num_raindrops)]

x_positions3 = [x_africa + np.random.uniform(-x_spread/2, x_spread/2) for _ in range(num_raindrops)]
y_positions3 = [y_africa + y_height + np.random.uniform(0, y_height) for _ in range(num_raindrops)]


# Create source for the raindrops
raindrop_source = ColumnDataSource(data=dict(
    x=x_positions,
    y=y_positions,
    url=['https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/animated-raindrop.svg'] * num_raindrops
))

snow_source = ColumnDataSource(data=dict(
    x=x_positions2,
    y=y_positions2,
    url=['https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/snowflake_2__83639.webp'] * num_raindrops
))

sun_source = ColumnDataSource(data=dict(
    x=x_positions3,
    y=y_positions3,
    url=['https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/sun.svg'] * num_raindrops
))
# Add the raindrops
raindrops = p.image_url(url='url', x='x', y='y', w=200000, h=200000,
                       source=raindrop_source, anchor="center")
snow = p.image_url(url='url', x='x', y='y', w=200000, h=200000,
                       source=snow_source, anchor="center")
sun = p.image_url(url='url', x='x', y='y', w=200000, h=200000,
                       source=sun_source, anchor="center")

# Set the plot ranges
x_range_min, _ = to_web_mercator(-20, 0)
x_range_max, _ = to_web_mercator(40, 0)
_, y_range_min = to_web_mercator(0, 10)
_, y_range_max = to_web_mercator(0, 80)
p.x_range.start = x_range_min
p.x_range.end = x_range_max
p.y_range.start = y_range_min
p.y_range.end = y_range_max

# Animation callback
def update():
    new_y = list(raindrop_source.data['y'])
    new_x = list(raindrop_source.data['x'])
    new_y2 = list(snow_source.data['y'])
    new_x2 = list(snow_source.data['x'])
    new_y3 = list(sun_source.data['y'])
    new_x3 = list(sun_source.data['x'])
    for i in range(len(new_y)):
        # Move raindrop down
        new_y[i] -= fall_speed
        new_y2[i] -= fall_speed
        new_y3[i] -= 0

        # If reached bottom, reset to random position at top
        if new_y[i] <= y_europe:
            new_x[i] = x_europe + np.random.uniform(-x_spread/2, x_spread/2)
            new_y[i] = y_europe + y_height + np.random.uniform(0, y_height/2)
    
        if new_y2[i] <= y_north:
            new_x2[i] = x_north + np.random.uniform(-x_spread/2, x_spread/2)
            new_y2[i] = y_north + y_height + np.random.uniform(0, y_height/2)


    raindrop_source.data.update(x=new_x, y=new_y)
    snow_source.data.update(x=new_x2, y=new_y2)

# Animation control
callback_id = None

def start_animation():
    global callback_id
    callback_id = curdoc().add_periodic_callback(update, 50)  # 50ms = 20fps
    start_button.disabled = True
    stop_button.disabled = False

def stop_animation():
    global callback_id
    if callback_id is not None:
        curdoc().remove_periodic_callback(callback_id)
    start_button.disabled = False
    stop_button.disabled = True

# Create buttons
start_button = Button(label='Start', button_type='primary')
stop_button = Button(label='Stop', button_type='danger', disabled=True)

start_button.on_click(start_animation)
stop_button.on_click(stop_animation)

# Layout
layout = column(row(start_button, stop_button), p)

# Add to document
curdoc().add_root(layout)
