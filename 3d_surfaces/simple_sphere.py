
import numpy as np
from bokeh.io import show, output_file
from bokeh.layouts import column, row
from bokeh.models import Slider, Select, TextInput, Button, CheckboxGroup, CustomJS, ColorBar, LinearColorMapper
from bokeh.models.tickers import BasicTicker
from surface_globe import create_globe

# Generate data
n_lat, n_lon = 30, 60
lats = np.linspace(-90, 90, n_lat)
lons = np.linspace(-180, 180, n_lon)
lon_grid, lat_grid = np.meshgrid(lons, lats)

# Temperature pattern
temps = 30 - 50 * np.abs(lat_grid) / 90
temps += 10 * np.sin(np.radians(lon_grid) * 3) * np.cos(np.radians(lat_grid) * 2)

# Flatten
lons_flat = lon_grid.flatten().tolist()
lats_flat = lat_grid.flatten().tolist()
temps_flat = temps.flatten().tolist()

# Create the globe widget
globe = create_globe(
    lons=lons_flat,
    lats=lats_flat,
    values=temps_flat,
    n_lat=n_lat,
    n_lon=n_lon,
    projection='sphere',
    palette='Turbo256',
    autorotate=True,
    show_coastlines=True,
    enable_hover=True,
    width=1200,
    height=800
)
show(globe)
