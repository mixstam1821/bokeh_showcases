# https://discourse.bokeh.org/t/rotating-the-sphere-automatically-or-manually/12505/2

import xarray as xr 
import numpy as np
import cartopy.crs as ccrs
from bokeh.plotting import figure, curdoc
from bokeh.models import ColorBar, LinearColorMapper, InlineStyleSheet, ColumnDataSource,Div, GlobalInlineStyleSheet
import cartopy.feature as cf
from bokeh.layouts import column
import pandas as pd
from matplotlib import cm
from matplotlib.colors import to_hex

curdoc().theme = 'dark_minimal'
gstyle = GlobalInlineStyleSheet(css=""" html, body, .bk, .bk-root {background-color: #15191c; margin: 0; padding: 0; height: 100%; color: white; font-family: 'Consolas', 'Courier New', monospace; } .bk { color: white; } .bk-input, .bk-btn, .bk-select, .bk-slider-title, .bk-headers, .bk-label, .bk-title, .bk-legend, .bk-axis-label { color: white !important; } .bk-input::placeholder { color: #aaaaaa !important; } """)
slider_style = InlineStyleSheet(css=""" /* Host slider container */ :host { background: none !important; } /* Full track: set dark grey, but filled part will override with .noUi-connect */ :host .noUi-base, :host .noUi-target { background: #bfbfbf !important; } /* Highlighted portion of track */ :host .noUi-connect { background: #00ffe0; } /* Slider handle */ :host .noUi-handle { background: #343838; border: 2px solid #00ffe0; border-radius: 50%; width: 20px; height: 20px; } /* Handle hover/focus */ :host .noUi-handle:hover, :host .noUi-handle:focus { border-color: #ff2a68; box-shadow: 0 0 10px #ff2a6890; } /* Tooltip stepping value */ :host .noUi-tooltip { background: #343838; color: #00ffe0; font-family: 'Consolas', monospace; border-radius: 6px; border: 1px solid #00ffe0; } /* Filled (active) slider track */ :host .noUi-connect { background: linear-gradient(90deg, #ffdd30 20%, #fc3737 100%) !important; /* greenish-cyan fade */ box-shadow: 0 0 10px #00ffe099 !important; } """)

# --- Define grid dimensions
n_lon = 576   ;   n_lat = 351   ;   n_years = 46  

# --- Generate lat/lon values
lon = np.linspace(-180, 180, n_lon, endpoint=False)
lat = np.linspace(-90, 90, n_lat)
years = np.arange(1979, 1979 + n_years)

base_pattern = 0.2 * np.cos(np.radians(np.meshgrid(lat, lon, indexing='ij')[0])) + 5 * np.sin(np.radians(2 * np.meshgrid(lat, lon, indexing='ij')[1]))
data = np.empty((n_years, n_lat, n_lon))

for i, yr in enumerate(years):
    data[i] = base_pattern + 0.05*(yr-1979) + np.random.normal(0, 0.5, (n_lat, n_lon))

# --- Build xarray DataArray
ds = xr.DataArray(
    data,
    coords={'year': years, 'lat': lat, 'lon': lon},
    dims=['year', 'lat', 'lon'],
    name='temperature'
)

# --- Calculate annual anomaly for 2024
yearly = ds
anomyearmean = yearly.sel(year=2024) - yearly.mean('year')

LON, LAT = np.meshgrid(lon, lat)
temperature = anomyearmean.values  


# FILL THE EMPTY LATS AT LON=-180
if not np.isclose(LON[0,0], LON[0,-1]):
    # Add a wrapped column at the end
    LON = np.hstack([LON, LON[:,0:1]])
    LAT = np.hstack([LAT, LAT[:,0:1]])
    temperature = np.hstack([temperature, temperature[:,0:1]])

# My color palette
rdblue256 = [to_hex(cm.get_cmap('RdBu_r')(i/255)) for i in range(256)]

projection = ccrs.Orthographic()
x, y = projection.transform_points(ccrs.PlateCarree(), LON, LAT)[:, :, :2].reshape(-1, 2).T
x_flat = x.flatten()
y_flat = y.flatten()
values_flat = temperature.flatten()
df = pd.DataFrame({'x': x_flat, 'y': y_flat, 'value': values_flat})
source = ColumnDataSource(df)
# Pre-compute all rotation positions
center_lon = 0
center_lat = 0
rotation_speed = 30  # Changed to 60 for easier pre-computation
current_step = 0
# Calculate number of steps for full rotation
steps = 360 // rotation_speed  # 6 steps
print(f"Pre-computing {steps} rotation positions...")

projection = ccrs.Orthographic(central_latitude=center_lat, central_longitude=center_lon)

# initialize coastlines
x_coords = []
y_coords = []
for coord_seq in cf.COASTLINE.geometries():
    # Convert coordinates to NumPy arrays
    lons = np.array([k[0] for k in coord_seq.coords])
    lats = np.array([k[1] for k in coord_seq.coords])
    
    # Transform coordinates
    transformed = projection.transform_points(ccrs.PlateCarree(), lons, lats)
    
    x_coords.extend(transformed[:, 0].tolist() + [np.nan])
    y_coords.extend(transformed[:, 1].tolist() + [np.nan])
coast_source = ColumnDataSource(data=dict(x=x_coords, y=y_coords))


precomputed_coastlines = []
precomputed_data = []
for angle in range(0, 360+1, rotation_speed):
    projection = ccrs.Orthographic(central_longitude=angle, central_latitude=center_lat)
    x_coords = []
    y_coords = []
    for coord_seq in cf.COASTLINE.geometries():
        # Convert coordinates to NumPy arrays
        lons = np.array([k[0] for k in coord_seq.coords])
        lats = np.array([k[1] for k in coord_seq.coords])
        
        # Transform coordinates
        transformed = projection.transform_points(ccrs.PlateCarree(), lons, lats)
        
        x_coords.extend(transformed[:, 0].tolist() + [np.nan])
        y_coords.extend(transformed[:, 1].tolist() + [np.nan])
    precomputed_coastlines.append({'x': x_coords, 'y': y_coords})

    # Convert to Robinson projection coordinates
    x, y = projection.transform_points(ccrs.PlateCarree(), LON, LAT)[:, :, :2].reshape(-1, 2).T

    # Flatten arrays for Bokeh
    x_flat = x.flatten()
    y_flat = y.flatten()
    values_flat = temperature.flatten()
    precomputed_data.append({'x': x_flat, 'y': y_flat, 'value': values_flat})  


minval = -3; maxval = 3
# Set up Bokeh plot
p_globe = figure(
    width=500, height=500,
    x_axis_type=None, y_axis_type=None,
    match_aspect=True,
    toolbar_location=None,
    background_fill_color='#15191c', output_backend='webgl'
)
p_globe.scatter(x='x', y='y', size=4, marker = 'square', color={'field': 'value', 'transform': LinearColorMapper(palette=rdblue256, low=minval, high=maxval)}, source=source)

p_globe.grid.visible = False
p_globe.axis.visible = False
p_globe.outline_line_color = '#15191c'
p_globe.background_fill_color = '#15191c'
color_mapper = LinearColorMapper(palette=rdblue256, low=minval, high=maxval)
color_bar = ColorBar(color_mapper=color_mapper, width=12, location=(0,0))
p_globe.add_layout(color_bar, 'right')

# COASTLINES
p_globe.line(x='x', y='y', source=coast_source, color="black", line_width=1, line_alpha=1)

def update_globe():
    global current_step
    # print(current_step)
    current_step = (current_step + 1) % steps
    source.data = precomputed_data[current_step]
    coast_source.data = precomputed_coastlines[current_step]

curdoc().add_periodic_callback(update_globe, 1000)  

gradient_text = """ <div style=" font-size: 18px; font-weight: bold; background: linear-gradient(90deg, red, orange, yellow); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; color: transparent; "> ERA5 Annual Mean Temperature Anomaly for 2024<br>compared to 1979-2024 (°C) </div> """
divinfo = Div(text = gradient_text)
layout = column(divinfo, p_globe, stylesheets = [gstyle])
curdoc().add_root(layout)









# MANUALLY ROTATION
import xarray as xr 
import numpy as np
import cartopy.crs as ccrs
from bokeh.plotting import figure, curdoc
from bokeh.models import ColorBar, LinearColorMapper, Slider, InlineStyleSheet, ColumnDataSource,Div, GlobalInlineStyleSheet

from bokeh.layouts import column
import pandas as pd
import cartopy.feature as cf
from matplotlib import cm
from matplotlib.colors import to_hex

curdoc().theme = 'dark_minimal'
gstyle = GlobalInlineStyleSheet(css=""" html, body, .bk, .bk-root {background-color: #15191c; margin: 0; padding: 0; height: 100%; color: white; font-family: 'Consolas', 'Courier New', monospace; } .bk { color: white; } .bk-input, .bk-btn, .bk-select, .bk-slider-title, .bk-headers, .bk-label, .bk-title, .bk-legend, .bk-axis-label { color: white !important; } .bk-input::placeholder { color: #aaaaaa !important; } """)
slider_style = InlineStyleSheet(css=""" /* Host slider container */ :host { background: none !important; } /* Full track: set dark grey, but filled part will override with .noUi-connect */ :host .noUi-base, :host .noUi-target { background: #bfbfbf !important; } /* Highlighted portion of track */ :host .noUi-connect { background: #00ffe0; } /* Slider handle */ :host .noUi-handle { background: #343838; border: 2px solid #00ffe0; border-radius: 50%; width: 20px; height: 20px; } /* Handle hover/focus */ :host .noUi-handle:hover, :host .noUi-handle:focus { border-color: #ff2a68; box-shadow: 0 0 10px #ff2a6890; } /* Tooltip stepping value */ :host .noUi-tooltip { background: #343838; color: #00ffe0; font-family: 'Consolas', monospace; border-radius: 6px; border: 1px solid #00ffe0; } /* Filled (active) slider track */ :host .noUi-connect { background: linear-gradient(90deg, #ffdd30 20%, #fc3737 100%) !important; /* greenish-cyan fade */ box-shadow: 0 0 10px #00ffe099 !important; } """)


# --- Define grid dimensions
n_lon = 576   ;   n_lat = 351   ;   n_years = 46  

# --- Generate lat/lon values
lon = np.linspace(-180, 180, n_lon, endpoint=False)
lat = np.linspace(-90, 90, n_lat)
years = np.arange(1979, 1979 + n_years)

base_pattern = 0.2 * np.cos(np.radians(np.meshgrid(lat, lon, indexing='ij')[0])) + 5 * np.sin(np.radians(2 * np.meshgrid(lat, lon, indexing='ij')[1]))
data = np.empty((n_years, n_lat, n_lon))

for i, yr in enumerate(years):
    data[i] = base_pattern + 0.05*(yr-1979) + np.random.normal(0, 0.5, (n_lat, n_lon))

# --- Build xarray DataArray
ds = xr.DataArray(
    data,
    coords={'year': years, 'lat': lat, 'lon': lon},
    dims=['year', 'lat', 'lon'],
    name='temperature'
)

# --- Calculate annual anomaly for 2024
yearly = ds
anomyearmean = yearly.sel(year=2024) - yearly.mean('year')
LON, LAT = np.meshgrid(lon, lat)
temperature = anomyearmean.values  # shape (n_lat, n_lon)
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# FILL THE EMPTY LATS AT LON=-180
if not np.isclose(LON[0,0], LON[0,-1]):
    # Add a wrapped column at the end
    LON = np.hstack([LON, LON[:,0:1]])
    LAT = np.hstack([LAT, LAT[:,0:1]])
    temperature = np.hstack([temperature, temperature[:,0:1]])

# My color palette
rdblue256 = [to_hex(cm.get_cmap('RdBu_r')(i/255)) for i in range(256)]


LON, LAT = np.meshgrid(lon, lat)
temperature = anomyearmean.values  


# FILL THE EMPTY LATS AT LON=-180
if not np.isclose(LON[0,0], LON[0,-1]):
    # Add a wrapped column at the end
    LON = np.hstack([LON, LON[:,0:1]])
    LAT = np.hstack([LAT, LAT[:,0:1]])
    temperature = np.hstack([temperature, temperature[:,0:1]])

# My color palette
rdblue256 = [to_hex(cm.get_cmap('RdBu_r')(i/255)) for i in range(256)]

projection = ccrs.Orthographic()
x, y = projection.transform_points(ccrs.PlateCarree(), LON, LAT)[:, :, :2].reshape(-1, 2).T
x_flat = x.flatten()
y_flat = y.flatten()
values_flat = temperature.flatten()
df = pd.DataFrame({'x': x_flat, 'y': y_flat, 'value': values_flat})
source = ColumnDataSource(df)
# Pre-compute all rotation positions
center_lon = 0
center_lat = 0
rotation_speed = 30  # Changed to 60 for easier pre-computation
current_step = 0
# Calculate number of steps for full rotation
steps = 360 // rotation_speed  # 6 steps
print(f"Pre-computing {steps} rotation positions...")

projection = ccrs.Orthographic(central_latitude=center_lat, central_longitude=center_lon)

# initialize coastlines
x_coords = []
y_coords = []
for coord_seq in cf.COASTLINE.geometries():
    # Convert coordinates to NumPy arrays
    lons = np.array([k[0] for k in coord_seq.coords])
    lats = np.array([k[1] for k in coord_seq.coords])
    
    # Transform coordinates
    transformed = projection.transform_points(ccrs.PlateCarree(), lons, lats)
    
    x_coords.extend(transformed[:, 0].tolist() + [np.nan])
    y_coords.extend(transformed[:, 1].tolist() + [np.nan])

coast_source = ColumnDataSource(data=dict(x=x_coords, y=y_coords))

minval = -3; maxval = 3

# Set up Bokeh plot
p_globe = figure(
    width=500, height=500,
    x_axis_type=None, y_axis_type=None,
    match_aspect=True,
    toolbar_location=None,
    background_fill_color='#15191c', output_backend='webgl'
)
p_globe.scatter(x='x', y='y', size=4, marker = 'square', color={'field': 'value', 'transform': LinearColorMapper(palette=rdblue256, low=minval, high=maxval)}, source=source)

p_globe.grid.visible = False
p_globe.axis.visible = False
p_globe.outline_line_color = '#15191c'
p_globe.background_fill_color = '#15191c'
color_mapper = LinearColorMapper(palette=rdblue256, low=minval, high=maxval)
color_bar = ColorBar(color_mapper=color_mapper, width=12, location=(0,0))
p_globe.add_layout(color_bar, 'right')

# COASTLINES
p_globe.line(x='x', y='y', source=coast_source, color="black", line_width=1, line_alpha=1)

# === SLIDERS ===
lon_slider = Slider(title="Longitude", start=-180, end=180, value=center_lon, step=1,  stylesheets = [slider_style])
lat_slider = Slider(title="Latitude", start=-90, end=90, value=center_lat, step=1, stylesheets = [slider_style])


def dataonsli(LATq,LONq):
    projection = ccrs.Orthographic(central_longitude=LONq, central_latitude=LATq)
    x_coords = []
    y_coords = []
    for coord_seq in cf.COASTLINE.geometries():
        # Convert coordinates to NumPy arrays
        lons = np.array([k[0] for k in coord_seq.coords])
        lats = np.array([k[1] for k in coord_seq.coords])
        
        # Transform coordinates
        transformed = projection.transform_points(ccrs.PlateCarree(), lons, lats)
        
        x_coords.extend(transformed[:, 0].tolist() + [np.nan])
        y_coords.extend(transformed[:, 1].tolist() + [np.nan])
    precomputed_coastlines = {'x': x_coords, 'y': y_coords}

    # Convert to Robinson projection coordinates
    x, y = projection.transform_points(ccrs.PlateCarree(), LON, LAT)[:, :, :2].reshape(-1, 2).T

    # Flatten arrays for Bokeh
    x_flat = x.flatten()
    y_flat = y.flatten()
    values_flat = temperature.flatten()
    precomputed_data = {'x': x_flat, 'y': y_flat, 'value': values_flat}
    return precomputed_data,precomputed_coastlines


def slider_update(attr, old, new):
    lon = lon_slider.value
    lat = lat_slider.value
    # Update rectangles and coastlines
    source.data = dataonsli(lat,lon)[0]
    coast_source.data = dataonsli(lat,lon)[1]

lon_slider.on_change('value_throttled', slider_update)
lat_slider.on_change('value_throttled', slider_update)

# Gradient label
gradient_text = """ <div style=" font-size: 18px; font-weight: bold; background: linear-gradient(90deg, red, orange, yellow); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; color: transparent; "> ERA5 Annual Mean Temperature Anomaly for 2024<br>compared to 1979-2024 (°C) </div> """
divinfo = Div(text = gradient_text)

controls = column(lon_slider, lat_slider)
layout = column(divinfo, p_globe, controls, stylesheets = [gstyle])

curdoc().add_root(layout)
