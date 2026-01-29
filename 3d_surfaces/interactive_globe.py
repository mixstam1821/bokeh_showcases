"""
Interactive SurfaceGlobe with full controls and colorbar
"""
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
    autorotate=False,
    show_coastlines=True,
    enable_hover=True,
    width=750,
    height=800
)

# Create colorbar
color_mapper = LinearColorMapper(palette="Turbo256", low=temps.min(), high=temps.max())
color_bar = ColorBar(
    color_mapper=color_mapper,
    ticker=BasicTicker(desired_num_ticks=10),
    width=30,
    height=700,
    location=(0, 0),
    title="Temperature (°C)",
    title_text_font_size="12pt",
    label_standoff=10
)

# ===== CONTROLS =====

# Rotation slider (disabled for flat projections)
rotation_slider = Slider(
    start=0, end=360, value=0, step=5,
    title="Rotation (°)",
    width=300
)

# Tilt slider
tilt_slider = Slider(
    start=-90, end=90, value=0, step=5,
    title="Tilt (°)",
    width=300
)

# Zoom slider
zoom_slider = Slider(
    start=0.5, end=3.0, value=1.0, step=0.1,
    title="Zoom (Mouse wheel also works!)",
    width=300
)

# Rotation speed slider
rotation_speed_slider = Slider(
    start=0.1, end=5.0, value=1.0, step=0.1,
    title="Rotation Speed",
    width=300
)

# Projection dropdown
projection_select = Select(
    title="Projection",
    value="sphere",
    options=["sphere", "mollweide", "natural_earth", "plate_carree"],
    width=180
)

# Palette dropdown
palette_select = Select(
    title="Color Palette",
    value="Turbo256",
    options=["Turbo256", "Viridis256", "Plasma256", "Inferno256", "Cividis256"],
    width=180
)

# vmin input
vmin_input = TextInput(
    title="vmin (leave empty for auto)",
    value="",
    width=180
)

# vmax input
vmax_input = TextInput(
    title="vmax (leave empty for auto)",
    value="",
    width=180
)

# Auto-rotate toggle button
autorotate_button = Button(
    label="▶ Start Auto-Rotate",
    button_type="success",
    width=180
)

# Apply button
apply_button = Button(
    label="Apply Settings",
    button_type="primary",
    width=180
)

# Hover checkbox
hover_checkbox = CheckboxGroup(
    labels=["Enable Hover Tooltip"],
    active=[0],
    width=180
)

# ===== CALLBACKS =====

# Link sliders to globe properties
rotation_slider.js_link('value', globe, 'rotation')
tilt_slider.js_link('value', globe, 'tilt')
zoom_slider.js_link('value', globe, 'zoom')
rotation_speed_slider.js_link('value', globe, 'rotation_speed')

# Projection change callback - disable rotation for flat projections
projection_callback = CustomJS(
    args=dict(globe=globe, rotation_slider=rotation_slider, tilt_slider=tilt_slider, 
              rotation_speed_slider=rotation_speed_slider, autorotate_button=autorotate_button),
    code="""
    const projection = cb_obj.value;
    globe.projection = projection;
    
    if (projection === 'sphere' || projection === 'surface_3d') {
        // Enable rotation controls for sphere and 3D surfaces
        rotation_slider.disabled = false;
        rotation_speed_slider.disabled = false;
        tilt_slider.disabled = (projection === 'sphere');
    } else {
        // Disable rotation controls for flat map projections
        rotation_slider.disabled = true;
        rotation_speed_slider.disabled = true;
        tilt_slider.disabled = true;
        globe.autorotate = false;
        autorotate_button.label = '▶ Start Auto-Rotate';
        autorotate_button.button_type = 'success';
    }
    """
)
projection_select.js_on_change('value', projection_callback)

# Palette change callback
palette_callback = CustomJS(
    args=dict(globe=globe),
    code="""
    globe.palette = cb_obj.value;
    """
)
palette_select.js_on_change('value', palette_callback)

# Auto-rotate toggle callback
autorotate_callback = CustomJS(
    args=dict(globe=globe),
    code="""
    const is_autorotating = globe.autorotate;
    
    if (is_autorotating) {
        // Stop auto-rotation
        globe.autorotate = false;
        cb_obj.label = '▶ Start Auto-Rotate';
        cb_obj.button_type = 'success';
    } else {
        // Start auto-rotation (only if sphere)
        if (globe.projection === 'sphere') {
            globe.autorotate = true;
            cb_obj.label = '⏸ Stop Auto-Rotate';
            cb_obj.button_type = 'warning';
        }
    }
    """
)
autorotate_button.js_on_click(autorotate_callback)

# Apply button callback (for vmin/vmax)
apply_callback = CustomJS(
    args=dict(globe=globe, vmin_input=vmin_input, vmax_input=vmax_input),
    code="""
    const vmin_str = vmin_input.value;
    const vmax_str = vmax_input.value;
    
    // Parse vmin
    if (vmin_str === '' || vmin_str === null) {
        globe.vmin = NaN;  // Auto
    } else {
        const parsed = parseFloat(vmin_str);
        if (!isNaN(parsed)) {
            globe.vmin = parsed;
        }
    }
    
    // Parse vmax
    if (vmax_str === '' || vmax_str === null) {
        globe.vmax = NaN;  // Auto
    } else {
        const parsed = parseFloat(vmax_str);
        if (!isNaN(parsed)) {
            globe.vmax = parsed;
        }
    }
    """
)
apply_button.js_on_click(apply_callback)

# Hover checkbox callback
hover_callback = CustomJS(
    args=dict(globe=globe),
    code="""
    globe.enable_hover = cb_obj.active.includes(0);
    """
)
hover_checkbox.js_on_change('active', hover_callback)

# ===== LAYOUT =====

# Add colorbar to globe
from bokeh.plotting import figure
dummy_fig = figure(width=30, height=700, toolbar_location=None, min_border=0)
dummy_fig.add_layout(color_bar, 'right')
dummy_fig.axis.visible = False
dummy_fig.grid.visible = False
dummy_fig.outline_line_color = None

# Main visualization row
viz_row = row(globe, dummy_fig)

# Controls layout
controls_row1 = row(rotation_slider, tilt_slider)
controls_row2 = row(zoom_slider, rotation_speed_slider)
controls_row3 = row(projection_select, palette_select, autorotate_button)
controls_row4 = row(vmin_input, vmax_input, apply_button)
controls_row5 = row(hover_checkbox)

controls = column(
    controls_row1,
    controls_row2,
    controls_row3,
    controls_row4,
    controls_row5
)

# Main layout
layout = column(viz_row, controls)

# Save and show
output_file("interactive_globe.html")
show(layout)

print("""
🌍 Interactive Globe with Colorbar:
====================================
✨ INTERACTION:
- Sphere/Surface 3D: Drag to rotate/tilt
- Flat Projections: Drag to pan (move viewport)
- Mouse Wheel: Zoom in/out (all projections)

📊 Projections Available:
- sphere: Interactive 3D globe (drag to rotate)
- mollweide: Equal-area elliptical (drag to pan)
- natural_earth: Designed by Tom Patterson (drag to pan)
- plate_carree: Simple equirectangular (drag to pan)

🎨 Controls:
- Rotation: Sphere/Surface only (disabled for maps)
- Tilt: Sphere/Surface only
- Zoom: All projections
- Projection: Switch between views
- Palette: Change color scheme
- Auto-Rotate: Sphere only (continues from current position)
- Hover Tooltip: Toggle on/off
""") 
