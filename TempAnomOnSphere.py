
# https://discourse.bokeh.org/t/temperature-anomalies-on-sphere-projection/12503
import xarray as xr 
import numpy as np
import cartopy.crs as ccrs
from bokeh.plotting import figure, show, curdoc, output_file, save
from bokeh.models import ColorBar, LinearColorMapper, BasicTicker, HoverTool, ColumnDataSource,Div, GlobalInlineStyleSheet
from bokeh.palettes import Turbo256
from bokeh.layouts import row, column
import pandas as pd
import cartopy.feature as cf
from matplotlib import cm
from matplotlib.colors import to_hex
curdoc().theme = 'dark_minimal'
gstyle = GlobalInlineStyleSheet(css=""" html, body, .bk, .bk-root {background-color: #15191c; margin: 0; padding: 0; height: 100%; color: white; font-family: 'Consolas', 'Courier New', monospace; } .bk { color: white; } .bk-input, .bk-btn, .bk-select, .bk-slider-title, .bk-headers, .bk-label, .bk-title, .bk-legend, .bk-axis-label { color: white !important; } .bk-input::placeholder { color: #aaaaaa !important; } """)

# === Load and process data ===
ds = xr.open_dataset('/home/michael/Downloads/ee574e584b1f8351c52f63525a06f50d.nc')['t2m']

yearly = ds.groupby('time.year').mean('time')
anomyearmean = yearly.sel(year=slice(2024,2024)).mean('year')-yearly.mean('year')
spatial_avg = yearly.weighted(np.cos(np.deg2rad(ds.lat))).mean(( 'lat',"lon"))
anoyear = spatial_avg - spatial_avg.mean('year')

lon = yearly.lon.values
lat = yearly.lat.values
LON, LAT = np.meshgrid(lon, lat)
temperature = anomyearmean.values
# temperature = 20 * np.cos(np.radians(LAT)) + 5 * np.sin(np.radians(2 * LON)) + np.random.normal(0, 1, LAT.shape)

# FILL THE EMPTY LATS AT LON=-180
if not np.isclose(LON[0,0], LON[0,-1]):
    # Add a wrapped column at the end
    LON = np.hstack([LON, LON[:,0:1]])
    LAT = np.hstack([LAT, LAT[:,0:1]])
    temperature = np.hstack([temperature, temperature[:,0:1]])

# My color palette
rdblue256 = [to_hex(cm.get_cmap('RdBu_r')(i/255)) for i in range(256)]


# DUMMY FOR UNIQUE COLORBAR
color_mapper = LinearColorMapper(palette=rdblue256,low=-3, high=3) #low=np.nanmin(temperature), high=-np.nanmin(temperature))
colorbar_fig = figure(width=70, height=1000, toolbar_location=None,
                      min_border=0,outline_line_color=None, background_fill_color="#15191c",
                      )
colorbar_fig.grid.visible = False
colorbar_fig.axis.visible = False
colorbar_fig.line([0, 0], [0, 0], line_width=0, line_color="white")
color_bar = ColorBar(color_mapper=color_mapper,
                     ticker=BasicTicker(),
                     label_standoff=12,
                     border_line_color=None,
                     background_fill_color="#15191c",
                     location=(0, 120),    height=800,

                     major_label_text_color="white"
                    )
colorbar_fig.add_layout(color_bar, 'right')

# === Globe projection ===

def visible_mask(lon, lat, center_lon, center_lat):
    lon = np.radians(lon)
    lat = np.radians(lat)
    clon = np.radians(center_lon)
    clat = np.radians(center_lat)
    x = np.cos(lat) * np.cos(lon)
    y = np.cos(lat) * np.sin(lon)
    z = np.sin(lat)
    cx = np.cos(clat) * np.cos(clon)
    cy = np.cos(clat) * np.sin(clon)
    cz = np.sin(clat)
    dot = x * cx + y * cy + z * cz
    return dot > 0


def make_sphere(LONq, LATq, title):
    projection = ccrs.Orthographic(central_latitude=LATq, central_longitude=LONq)
    x, y = projection.transform_points(ccrs.PlateCarree(), LON, LAT)[:, :, :2].reshape(-1, 2).T
    x_flat = x.flatten()
    y_flat = y.flatten()
    values_flat = temperature.flatten()
    df = pd.DataFrame({'x': x_flat, 'y': y_flat, 'value': values_flat})
    source = ColumnDataSource(df)

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
        width=400, height=400,
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
    # color_mapper = LinearColorMapper(palette=rdblue256, low=minval, high=maxval)
    # color_bar = ColorBar(color_mapper=color_mapper, width=12, location=(0,0))
    # p_globe.add_layout(color_bar, 'right')

    # COASTLINES
    p_globe.line(x='x', y='y', source=coast_source, color="black", line_width=1, line_alpha=1)

    return p_globe

# === Anomaly per year HBar ===
years = [str(y) for y in anoyear.year.values] # Convert to strings for categorical y
anomalies = anoyear.values
hbar_source = ColumnDataSource(data=dict(
    years=years,
    anomalies=anomalies,
    color=[Turbo256[int(255*(a - anomalies.min())/(anomalies.ptp()+1e-8))] for a in anomalies]
))

p_hbar = figure(y_range=years, height=800, width=400, x_range=(-0.6, 0.6),
                title="Global",
                x_axis_label="Anomaly (°C)", y_axis_label="Year",
                toolbar_location=None)
p_hbar.hbar(y='years', right='anomalies', left=0, height=0.9, color='color', source=hbar_source)
p_hbar.ygrid.grid_line_color = None
# p_hbar.xgrid.grid_line_dash = [6, 4]
p_hbar.grid.visible = False
p_hbar.title.text_font_size = '12pt'
p_hbar.xaxis.axis_label_text_font_size = "12pt"
p_hbar.yaxis.major_label_text_font_size = "10pt"
p_hbar.background_fill_color = '#15191c'
p_hbar.add_tools(HoverTool(
    tooltips=[
        ("Year", "@years"),
        ("Anomaly", "@anomalies{0.2f} °C")
    ]
))
p_hbar.outline_line_color = '#15191c'
p_hbar.title.align = "center"

p1 = make_sphere(-80, 0, 'Americas')
p2 = make_sphere(20, 0, 'Europe/Africa')
p3 = make_sphere(100, 0, 'Asia')
p4 = make_sphere(-160, 0, 'Pacific Ocean')
p5 = make_sphere(0, 90, 'Arctic')
p6 = make_sphere(0, -90, 'Antarctic')

gradient_text = """ <div style=" font-size: 28px; font-weight: bold; background: linear-gradient(90deg, red, orange, yellow); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; color: transparent; "> ERA5 Annual Mean Temperature Anomaly for 2024 compared to 1979-2024 (°C) </div> """
divinfo = Div(text = gradient_text)

# === Layout side by side and show ===
LL = column(divinfo,row(column(row(p1,p2,p5), row(p3,p4,p6)),colorbar_fig, p_hbar), stylesheets = [gstyle])
show(LL)
