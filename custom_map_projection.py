# please see also my post here: https://discourse.bokeh.org/t/custom-map-projection/12253/2

# simple map
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import LinearColorMapper, BasicTicker, ColorBar
from bokeh.palettes import linear_palette, interp_palette
from bokeh.models import ColumnDataSource, CustomJS,Circle, HoverTool, Div, DatetimeTickFormatter, NumeralTickFormatter, TextAreaInput


# Generate example data
longitudes = np.linspace(-180, 180, 576)
latitudes = np.linspace(-90, 90, 361)
LON, LAT = np.meshgrid(lon, lat)

# Create sample temperature data
temperatures = 20 * np.cos(np.radians(LAT)) + \
              5 * np.sin(np.radians(2 * LON)) + \
              np.random.normal(0, 1, LAT.shape)

mike2=('#000063','#123aff','#00aeff','#26fff4','#00ff95','#19ff19','#ffff00','#ff8a15','#ff2a1b','#db0000','#4b0000')
bo_mike2 = interp_palette(mike2, 255)

lats = np.repeat(latitudes, len(longitudes))
lons = np.tile(longitudes, len(latitudes))
s1 = ColumnDataSource(data={'image': [temperatures], 'latitudes': [lats], 'longitudes': [lons]})

def crd():
  import cartopy.feature as cf,numpy as np
  # create the list of coordinates separated by nan to avoid connecting the lines
  x_coords = []
  y_coords = []
  for coord_seq in cf.COASTLINE.geometries():
      x_coords.extend([k[0] for k in coord_seq.coords] + [np.nan])
      y_coords.extend([k[1] for k in coord_seq.coords] + [np.nan])
  return x_coords,y_coords,#x_coords2,y_coords2
x_coords,y_coords=[i for i in crd()]



color_mapper= LinearColorMapper(palette=bo_mike2, low=0, high=35)

plot = figure(x_range=(-180,180), y_range=(-90,90),active_scroll="wheel_zoom", output_backend="webgl",width=900)
r=plot.image(image='image', color_mapper=color_mapper, x=min(longitudes),
     y=min(latitudes),
     dw=max(longitudes) - min(longitudes),
     dh=max(latitudes) - min(latitudes),source = s1)
color_bar = ColorBar(color_mapper= color_mapper, ticker= BasicTicker(),location=(0,0));     plot.add_layout(color_bar, 'right')

plot.line(x = x_coords,y = y_coords, line_width=1, line_color='black')

plot.add_tools(HoverTool(renderers = [r],tooltips="""<font size="5"><i>Temp:</i> <b>@image</b> <br> <i>lat:</i> <b>@latitudes</b><br> <i>lon:</i> <b>@longitudes</b>""")) 

show(plot)


# Robinson
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from bokeh.plotting import figure, show
from bokeh.models import ColorBar, LinearColorMapper, BasicTicker, HoverTool, ColumnDataSource
from bokeh.palettes import Inferno256
from shapely.geometry import LineString, MultiLineString

# Generate example data
lon = np.linspace(-180, 180, 576)
lat = np.linspace(-90, 90, 361)
LON, LAT = np.meshgrid(lon, lat)

# Create sample temperature data
temperature = 20 * np.cos(np.radians(LAT)) + \
              5 * np.sin(np.radians(2 * LON)) + \
              np.random.normal(0, 1, LAT.shape)

# Set up Cartopy projection
projection = ccrs.Robinson()

# Convert to projection coordinates
transformed_points = projection.transform_points(ccrs.PlateCarree(), LON, LAT)
x = transformed_points[:, :, 0]
y = transformed_points[:, :, 1]

# Create the figure
p = figure(width=800, height=400, 
           title="Global Temperature Distribution (Robinson Projection)",
           x_range=(x.min(), x.max()), 
           y_range=(y.min(), y.max()))

# Create color mapper
color_mapper = LinearColorMapper(palette=Inferno256, 
                                 low=temperature.min(), 
                                 high=temperature.max())

# Create patches for grid cells
xs = []
ys = []
temps = []
for i in range(x.shape[0] - 1):
    for j in range(x.shape[1] - 1):
        # Get cell corners
        cell_x = [x[i,j], x[i,j+1], x[i+1,j+1], x[i+1,j]]
        cell_y = [y[i,j], y[i,j+1], y[i+1,j+1], y[i+1,j]]
        
        # Add valid cells
        if not np.any(np.isnan(cell_x)) and not np.any(np.isnan(cell_y)):
            xs.append(cell_x)
            ys.append(cell_y)
            temps.append(temperature[i,j])

# Create ColumnDataSource
source = ColumnDataSource(data=dict(
    xs=xs,
    ys=ys,
    temp=temps
))

# Add patches
patches = p.patches('xs', 'ys',
                    fill_color={'field': 'temp', 'transform': color_mapper},
                    line_color=None,
                    source=source)

# Add coastlines
coastlines = cfeature.NaturalEarthFeature('physical', 'coastline', '110m')

def process_line_string(line_string):
    if isinstance(line_string, (LineString, MultiLineString)):
        if isinstance(line_string, LineString):
            lines = [line_string]
        else:
            lines = list(line_string.geoms)
        
        for line in lines:
            coords = np.array(line.coords)
            if len(coords) > 1:
                # Normalize longitudes to -180 to 180 range
                normalized_coords = coords.copy()
                normalized_coords[:, 0] = np.mod(normalized_coords[:, 0] + 180, 360) - 180
                
                # Filter out points that are too close together or would create artifacts
                valid_indices = np.where(np.abs(np.diff(normalized_coords[:, 0])) < 180)[0]
                valid_indices = np.concatenate([valid_indices, [valid_indices[-1] + 1]])
                
                if len(valid_indices) > 1:
                    segment = normalized_coords[valid_indices]
                    
                    # Transform coordinates
                    tt = projection.transform_points(ccrs.PlateCarree(), 
                                                    segment[:, 0], 
                                                    segment[:, 1])
                    x = tt[:, 0]
                    y = tt[:, 1]
                    
                    # Only draw if we have enough points and they're not all NaN
                    if len(x) > 1 and not np.all(np.isnan(x)):
                        p.line(x, y, line_color='black', line_width=1, line_alpha=0.5)

for geom in coastlines.geometries():
    process_line_string(geom)

# Add hover tool
hover = HoverTool(tooltips=[
    ('Temperature', '@temp{0.1f}°C'),
], renderers=[patches])
p.add_tools(hover)

# Add color bar
color_bar = ColorBar(color_mapper=color_mapper,
                     ticker=BasicTicker(),
                     label_standoff=12,
                     border_line_color=None,
                     location=(0, 0))
p.add_layout(color_bar, 'right')

# Customize the plot
p.grid.visible = False
p.axis.visible = False
p.title.text_font_size = '14pt'

# Output the plot
show(p)






# Mollweide
import numpy as np
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColorBar, LinearColorMapper, BasicTicker, HoverTool, ColumnDataSource
from bokeh.palettes import Viridis256
import cartopy.feature as cfeature
from shapely.geometry import LineString, MultiLineString

def mollweide_transform(lon, lat):
    """Transform longitude and latitude to Mollweide projection coordinates."""
    # Convert to radians
    lon = np.radians(lon)
    lat = np.radians(lat)
    
    # Auxiliary angle theta
    theta = lat
    for i in range(100):  # Max iterations
        theta_new = theta - (2 * theta + np.sin(2 * theta) - np.pi * np.sin(lat)) / (2 + 2 * np.cos(2 * theta))
        if np.all(np.abs(theta - theta_new) < 1e-10):
            break
        theta = theta_new
    
    # Calculate x and y coordinates
    x = 2 * np.sqrt(2) / np.pi * lon * np.cos(theta)
    y = np.sqrt(2) * np.sin(theta)
    
    return x, y

# Create sample data with higher resolution
n_lat, n_lon = 180, 360  # Higher resolution for WebGL
lats = np.linspace(-89.5, 89.5, n_lat)
lons = np.linspace(-179.5, 179.5, n_lon)
lon_grid, lat_grid = np.meshgrid(lons, lats)

# Create sample temperature data (example: temperature variation with latitude)
temperature = 20 * np.cos(np.radians(lat_grid)) + \
             5 * np.sin(np.radians(2 * lon_grid)) + \
             np.random.normal(0, 1, (n_lat, n_lon))

# Create the figure with WebGL
p = figure(width=800, height=400, 
          title="Global Temperature Distribution (Mollweide Projection)",
          x_range=(-2.5, 2.5), y_range=(-1.3, 1.3),
          )  

# Create color mapper
color_mapper = LinearColorMapper(palette=Viridis256, 
                               low=np.min(temperature), 
                               high=np.max(temperature))

# Create patches for each grid cell
xs = []
ys = []
temps = []

for i in range(n_lat - 1):
    for j in range(n_lon - 1):
        # Get the four corners of the cell
        lons_cell = [lon_grid[i,j], lon_grid[i,j+1], lon_grid[i+1,j+1], lon_grid[i+1,j]]
        lats_cell = [lat_grid[i,j], lat_grid[i,j+1], lat_grid[i+1,j+1], lat_grid[i+1,j]]
        
        # Transform to Mollweide projection
        x, y = mollweide_transform(lons_cell, lats_cell)
        
        # Check if the cell crosses the date line
        if np.any(np.abs(np.diff(lons_cell)) > 180):
            continue
        
        # Add the cell if it's valid
        if not np.any(np.isnan(x)) and not np.any(np.isnan(y)):
            xs.append(x.tolist())
            ys.append(y.tolist())
            temps.append(temperature[i,j])

# Create ColumnDataSource
source = ColumnDataSource(data=dict(
    xs=xs,
    ys=ys,
    temp=temps
))

# Add the patches with WebGL
patches = p.patches('xs', 'ys',
                   fill_color={'field': 'temp', 'transform': color_mapper},
                   line_color=None,
                   source=source)

# Add coastlines
coastlines = cfeature.NaturalEarthFeature('physical', 'coastline', '110m')

def process_line_string(line_string):
    if isinstance(line_string, (LineString, MultiLineString)):
        if isinstance(line_string, LineString):
            lines = [line_string]
        else:
            lines = list(line_string.geoms)
        
        for line in lines:
            coords = np.array(line.coords)
            if len(coords) > 1:
                # Split at the dateline
                splits = np.where(np.abs(np.diff(coords[:, 0])) > 180)[0] + 1
                segments = np.split(coords, splits)
                
                for segment in segments:
                    if len(segment) > 1:
                        x, y = mollweide_transform(segment[:, 0], segment[:, 1])
                        p.line(x, y, line_color='black', line_width=1, line_alpha=0.5)

for geom in coastlines.geometries():
    process_line_string(geom)

# Add hover tool
hover = HoverTool(tooltips=[
    ('Temperature', '@temp{0.1f}°C'),
], renderers=[patches])
p.add_tools(hover)

# Add color bar
color_bar = ColorBar(color_mapper=color_mapper,
                    ticker=BasicTicker(),
                    label_standoff=12,
                    border_line_color=None,
                    location=(0, 0))
p.add_layout(color_bar, 'right')

# Customize the plot
p.grid.visible = False
p.axis.visible = False
p.title.text_font_size = '14pt'

# Add graticules (longitude and latitude lines)
for lat in np.arange(-75, 76, 15):
    lons = np.linspace(-180, 180, 100)
    x, y = mollweide_transform(lons, np.full_like(lons, lat))
    p.line(x, y, line_color='gray', line_alpha=0.3)

for lon in np.arange(-180, 181, 30):
    lats = np.linspace(-89.5, 89.5, 100)
    x, y = mollweide_transform(np.full_like(lats, lon), lats)
    p.line(x, y, line_color='gray', line_alpha=0.3)

# Add equator with different style
eq_x, eq_y = mollweide_transform(lons, np.zeros_like(lons))
p.line(eq_x, eq_y, line_color='gray', line_width=2, line_alpha=0.5)

# Output to file
# output_file("mollweide.html")
show(p)



