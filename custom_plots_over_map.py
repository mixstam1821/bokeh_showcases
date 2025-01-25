# https://discourse.bokeh.org/t/custom-plots-over-a-map/12257

from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, HoverTool, Legend
from bokeh.palettes import Spectral4
from bokeh.transform import cumsum
import numpy as np
import pandas as pd
from math import pi

# Convert to Web Mercator coordinates
def convert_to_mercator(lon, lat):
    """Convert longitude/latitude to Web Mercator coordinates"""
    k = 6378137
    x = lon * (k * pi/180.0)
    y = np.log(np.tan((90 + lat) * pi/360.0)) * k
    return x, y

# Define data for regions
regions = {
    "Europe": {
        "coords": (48.8566, 15.3522),
        "distribution": {"North America": 95, "South America": 65, "Central America": 35, "Caribbean": 5}
    },
    "Americas": {
        "coords": (-20.0000, -60.0000),
        "distribution": {"North America": 35, "South America": 85, "Central America": 35, "Caribbean": 15}
    },
    "Australia": {
        "coords": (-30.0000, 150.0000),
        "distribution": {"North America": 5, "South America": 65, "Central America": 45, "Caribbean": 35}
    }
}

# Prepare data for pie charts
pie_sources = []
for region, data in regions.items():
    lat, lon = data["coords"]
    x, y = convert_to_mercator(lon, lat)  # Convert to Mercator

    # Create pie chart data
    pie_data = pd.DataFrame.from_dict(data["distribution"], orient='index', columns=['value']).reset_index()
    pie_data['angle'] = pie_data['value'] / pie_data['value'].sum() * 2 * pi
    pie_data['color'] = Spectral4[:len(pie_data)]
    
    pie_sources.append({
        'name': region,
        'x': x,
        'y': y,
        'source': ColumnDataSource(pie_data),
        'color': pie_data['color']
    })

# Create vertical bars data 
vbar_data = {
    'x': [convert_to_mercator(regions["Australia"]['coords'][1]-90, regions["Australia"]['coords'][0])[0] + 1000000, 
          convert_to_mercator(regions["Australia"]['coords'][1]-88, regions["Australia"]['coords'][0])[0] + 2000000, 
          convert_to_mercator(regions["Australia"]['coords'][1]-86, regions["Australia"]['coords'][0])[0] + 3000000],
    'top': np.random.randint(300000, 3530000, size=3),  # Random height values for bars
    'color': ['#6dbcf5', '#63ff63', '#ec5c5c']
}

vbar_source = ColumnDataSource(vbar_data)

# Create main figure
p = figure(width=1000, height=800,
           title="Regional Overview",
           background_fill_color='#252525',
           border_fill_color='#252525',
           outline_line_color=None,
           x_range=(-18000000, 18000000), y_range=(-8000000, 8000000),
           x_axis_type="mercator", y_axis_type="mercator")

# Add map background (CartoDB Dark Matter)
p.add_tile("CartoDB Dark Matter", retina=True)

# Add pie charts (larger than city charts)
for region_data in pie_sources:
    p.wedge(x=region_data['x'], y=region_data['y'], radius=1000000,
            start_angle=cumsum('angle', include_zero=True),
            end_angle=cumsum('angle'),
            line_color="white", line_width=2,
            fill_color='color', source=region_data['source'],
            alpha=0.8, legend_field='index')

# Add vertical bars (vbar)
p.vbar(x='x', top='top', width=800000, color='color', source=vbar_source)

# Add hover tool for pie charts and bars
hover = HoverTool()
hover.tooltips = [("Region", "@index"), ("Value", "@value"), ("Height", "@top")]
p.add_tools(hover)

# Remove grid lines
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.xaxis.axis_line_color = None
p.yaxis.axis_line_color = None

# Output to file
output_file("geoplot2.html")
show(p)
