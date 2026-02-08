# https://discourse.bokeh.org/t/watching-earth-warm-in-flame-motion/12711

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, InlineStyleSheet, Label, Button, Div, Span
from bokeh.plotting import figure, curdoc
import numpy as np
from scipy.stats import norm, gaussian_kde
import xarray as xr
#Source: https://data.giss.nasa.gov/pub/gistemp/gistemp250_GHCNv4.nc.gz

# Global cache to prevent recomputation
_DATA_CACHE = {}

def load_and_precompute_data():
    """Load data and pre-compute distributions (cached)"""
    if 'all_distributions' in _DATA_CACHE:
        print("Using cached data...")
        return _DATA_CACHE
    
    print("Loading and pre-computing data for the first time...")
    
    # Load GISTEMP data
    ds = xr.open_dataset("/home/michael/Downloads/gistemp250_GHCNv4.nc")
    v = ds.variables['tempanomaly']

    # Get time information
    time_var = ds.variables['time']
    years = ds["time"].dt.year + (ds["time"].dt.month - 1) / 12.0

    # Filter data for 1970-2025
    year_start = 1970
    year_end = 2025
    valid_years = (years >= year_start) & (years <= year_end)
    years_filtered = years[valid_years]
    temp_data = v[valid_years, :, :]

    print(f"Loaded data from {years_filtered.min().values:.1f} to {years_filtered.max().values:.1f}")
    print(f"Data shape: {temp_data.shape}")

    # Create x-axis for temperature anomalies
    x_range = np.linspace(-8, 8, 2048)

    def compute_distribution_for_year(target_year):
        """Compute latitude-weighted Gaussian KDE fitted to real GISTEMP data"""
        
        # Find closest time index for target year
        year_idx = int(np.argmin(np.abs(years_filtered.values - target_year)))
        
        # Get latitude weights (account for different areas of 2x2 degree patches)
        lats = ds.variables['lat'][:].data
        lat_weights = np.cos(np.deg2rad(lats))
        
        # Get temperature anomalies for this year
        temp_slice = temp_data[year_idx, :, :]
        
        # Flatten and get valid data
        valid_mask = np.isfinite(temp_slice.values)
        valid_temps = temp_slice.values[valid_mask]
        
        # Create matching weights for valid temperatures
        lat_weights_2d = np.broadcast_to(lat_weights.reshape(-1, 1), temp_slice.shape)
        valid_weights = lat_weights_2d[valid_mask]
        
        if len(valid_temps) < 10:
            # Fallback
            mean_val = 0
            y_dist = norm.pdf(x_range, 0, 2.0)
            return y_dist, mean_val
        
        # Compute latitude-weighted Gaussian KDE
        kde = gaussian_kde(valid_temps, weights=valid_weights)
        y_dist = kde(x_range)
        
        # Compute weighted mean
        mean_val = np.average(valid_temps, weights=valid_weights)
        
        return y_dist, mean_val

    # Pre-compute all distributions for smooth interpolation
    print("Pre-computing distributions for all years...")
    all_years = list(range(year_start, year_end + 1))
    all_distributions = []
    all_means = []

    for year in all_years:
        y_dist, mean_val = compute_distribution_for_year(year)
        all_distributions.append(y_dist)
        all_means.append(mean_val)
        
    print(f"Pre-computed {len(all_distributions)} distributions")
    
    # Cache the results
    _DATA_CACHE['all_distributions'] = all_distributions
    _DATA_CACHE['all_means'] = all_means
    _DATA_CACHE['x_range'] = x_range
    _DATA_CACHE['year_start'] = year_start
    _DATA_CACHE['year_end'] = year_end
    
    return _DATA_CACHE

# Load data once
data = load_and_precompute_data()
all_distributions = data['all_distributions']
all_means = data['all_means']
x_range = data['x_range']
year_start = data['year_start']
year_end = data['year_end']

# Initialize with 1970
y_year = all_distributions[0]
mean_1970 = all_means[0]

# Create data sources
year_source = ColumnDataSource(data=dict(x=x_range, y=y_year))

# Create figure
p = figure(
    width=1200,
    height=700,
    title="Land Temperature Anomaly Distribution 1970-2025 (NASA GISTEMP Data)",
    x_axis_label="Temperature Anomaly (°C)",
    y_axis_label="Probability Density",
    x_range=(-4, 4),
    y_range=(0, .6),
    toolbar_location=None,
    tools=""
)

# Create masking areas
max_y = 100
dark_mask = "#000000"

# Mask above the curve
mask_source = ColumnDataSource(data=dict(x=x_range, y1=y_year, y2=[max_y]*len(x_range)))
mask_top = p.varea(
    x='x',
    y1='y1',
    y2='y2',
    source=mask_source,
    fill_color=dark_mask,
    fill_alpha=0.85,
)

# Mask before left bound
p.varea(
    x=np.linspace(-100, -4, 50),
    y1=-max_y,
    y2=max_y,
    fill_color=dark_mask,
    fill_alpha=0.85,
)

# Mask after right bound
p.varea(
    x=np.linspace(4, 100, 50),
    y1=-max_y,
    y2=max_y,
    fill_color=dark_mask,
    fill_alpha=0.85,
)

# Add vertical white line at x=0 (baseline reference)
zero_line = Span(location=0, dimension='height', line_color='white', 
                 line_width=2, line_alpha=0.8)
p.add_layout(zero_line)

# Add year curve outline (white line)
year_line = p.line(
    x='x',
    y='y',
    source=year_source,
    line_color='white',
    line_width=3,
    alpha=0.95,
)

# Add year label in the dark area (upper left corner)
year_label = Label(
    x=-3.5, y=0.5,
    text='1970',
    text_font_size='72pt',
    text_color='white',
    text_font_style='bold',
    text_alpha=1.0
)
p.add_layout(year_label)

# Add mean anomaly label below year (bright orange color)
mean_label = Label(
    x=-3.5, y=0.4,
    text=f'Mean: {mean_1970:.2f}°C',
    text_font_size='32pt',
    text_color='#FF6600',  # Bright orange
    text_font_style='bold',
    text_alpha=1.0
)
p.add_layout(mean_label)


referano = Label(
    x=-3.5, y=0.38,
    text="Reference Period: 1951-1980",
    text_font_size='12pt',
    text_color='lime',  
    text_font_style='italic',
    text_alpha=1.0
)
p.add_layout(referano)

# Styling
p.background_fill_color = None
p.border_fill_color = "#000000"
p.outline_line_color = "#444444"
p.grid.grid_line_color = "#333333"
p.grid.grid_line_alpha = 0

p.title.text_font_size = "20pt"
p.title.text_color = "#FFFFFF"
p.xaxis.axis_label_text_color = "#CCCCCC"
p.xaxis.axis_label_text_font_size = "14pt"
p.xaxis.major_label_text_font_size = "12pt"
p.yaxis.axis_label_text_color = "#CCCCCC"
p.xaxis.major_label_text_color = "#999999"
p.yaxis.major_label_text_color = "#999999"
p.xaxis.axis_line_color = "#666666"
p.yaxis.axis_line_color = "#666666"

# Show y-axis labels (density values)
p.yaxis.major_label_text_font_size = "12pt"
p.yaxis.major_label_text_color = "#999999"

gradient_css = """
:host {
  background: linear-gradient(to right,
    #041836 0%,    
    #08306B 12%,   
    #2171B5 28%,   
    #6BAED6 37%,  
    #9ECAE1 45%,   
    #ffffff 52%,   
    #FFF200 60%,   
    #FFAA00 70%,  
    #FB6A4A 80%,   
    #CB181D 90%,  
    #99000D 100%   
  );
}
"""

stylesheet = InlineStyleSheet(css=gradient_css)

# Create slider - INTEGER YEARS ONLY
slider = Slider(
    start=year_start, 
    end=year_end, 
    value=year_start, 
    step=1,  # Integer years only
    title="Year",
    width=1000
)

def update_year(year):
    """Update visualization for a specific year"""
    year = int(year)
    year_idx = year - year_start
    
    # Get pre-computed distribution
    y_year_new = all_distributions[year_idx]
    mean_year = all_means[year_idx]
    
    # Update sources
    year_source.data = dict(x=x_range, y=y_year_new)
    mask_source.data = dict(x=x_range, y1=y_year_new, y2=[max_y]*len(x_range))
    
    # Update labels
    p.title.text = f"Land Temperature Anomaly Distribution 1970-2025 (NASA GISTEMP Data)"
    year_label.text = str(year)
    mean_label.text = f'Mean: {mean_year:.2f}°C'

def slider_callback(attr, old, new):
    update_year(slider.value)

slider.on_change('value', slider_callback)

# Animation controls
play_button = Button(label="► Play", button_type="success", width=100)
pause_button = Button(label="⏸ Pause", button_type="warning", width=100)
reset_button = Button(label="↺ Reset", button_type="primary", width=100)


# Animation state with interpolation
animation_callback = None
current_year_idx = 0
interpolation_frame = 0
num_interpolation_frames = 10  # Number of frames to interpolate between years

def animate_smooth():
    """Smooth animation with interpolation between years"""
    global current_year_idx, interpolation_frame
    
    if interpolation_frame < num_interpolation_frames:
        # Interpolate between current and next year
        next_year_idx = min(current_year_idx + 1, len(all_distributions) - 1)
        
        t = interpolation_frame / num_interpolation_frames  # 0 to 1
        
        # Linear interpolation between distributions
        y_current = all_distributions[current_year_idx]
        y_next = all_distributions[next_year_idx]
        y_interpolated = y_current * (1 - t) + y_next * t
        
        # Interpolate mean
        mean_current = all_means[current_year_idx]
        mean_next = all_means[next_year_idx]
        mean_interpolated = mean_current * (1 - t) + mean_next * t
        
        # Update sources WITHOUT changing labels (keep integer year)
        year_source.data = dict(x=x_range, y=y_interpolated)
        mask_source.data = dict(x=x_range, y1=y_interpolated, y2=[max_y]*len(x_range))
        
        interpolation_frame += 1
    else:
        # Move to next year
        interpolation_frame = 0
        current_year_idx += 1
        
        if current_year_idx > len(all_distributions) - 1:
            # Loop back to start
            current_year_idx = 0
            slider.value = year_start
        else:
            # Update slider and labels to next integer year
            new_year = year_start + current_year_idx
            slider.value = new_year
            
            mean_year = all_means[current_year_idx]
            p.title.text = f"Land Temperature Anomaly Distribution 1970-2025 (NASA GISTEMP Data)"
            year_label.text = str(new_year)
            mean_label.text = f'Mean: {mean_year:.2f}°C'

def play_animation():
    """Start smooth animation"""
    global animation_callback, current_year_idx, interpolation_frame
    if animation_callback is None:
        current_year_idx = slider.value - year_start
        interpolation_frame = 0
        animation_callback = curdoc().add_periodic_callback(animate_smooth, 30)  # ~33 fps

def pause_animation():
    """Pause animation"""
    global animation_callback
    if animation_callback is not None:
        curdoc().remove_periodic_callback(animation_callback)
        animation_callback = None

def reset_animation():
    """Reset to 1970"""
    global current_year_idx, interpolation_frame
    pause_animation()
    current_year_idx = 0
    interpolation_frame = 0
    slider.value = year_start
    update_year(year_start)

play_button.on_click(play_animation)
pause_button.on_click(pause_animation)
reset_button.on_click(reset_animation)

# Layout
controls = row(play_button, pause_button, reset_button, Div(text='Source: https://data.giss.nasa.gov/pub/gistemp/gistemp250_GHCNv4.nc.gz'))
layout = column(
    slider,
    controls,
    column(p, stylesheets=[stylesheet])
)

# Add to document
curdoc().add_root(layout)
curdoc().title = "Temperature Anomaly Distribution 1970-2025 NASA GISTEMP Data"
