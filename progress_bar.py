# https://discourse.bokeh.org/t/progress-bar/12254

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.io import curdoc
import numpy as np

# Set your custom percentage here
TARGET_PERCENTAGE = 90

# Create data source for the progress bar
source = ColumnDataSource({
    'x': [0],
    'y': [0],
    'width': [0],
    'text': ['0%'],
    'text_x': [0]
})

# Create figure
p = figure(width=600, height=120,
           x_range=(0, 1), y_range=(-0.5, 0.5),
           tools="", toolbar_location=None)

# Remove axes and grid
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Background styling
p.background_fill_color = "#1A1A1A"
p.border_fill_color = "#1A1A1A"

# Add multiple glow layers for background bar
for alpha in [0.1, 0.05, 0.02]:
    size = 0.2 + (0.1 * (1-alpha))  # Increase size for outer glow
    p.hbar(y=0, right=1.0, height=size, border_radius=19,
           fill_color=None,
           line_color="#404040",
           line_width=2,
           line_alpha=alpha,
           line_cap="round",
           line_join="round")

# Add background bar (darker)
p.hbar(y=0, right=1.0, height=0.2, border_radius=19,
       fill_color="#2A2A2A",
       line_color="#404040",
       line_width=2,
       line_cap="round",
       line_join="round")

# Add multiple glow layers
glow_color = "#00FF00"  # Bright green for glow
for alpha in [0.1, 0.05, 0.02]:
    size = 0.2 + (0.1 * (1-alpha))  # Increase size for outer glow
    p.hbar(y=0, right='width', height=size, border_radius=19,
           source=source,
           fill_color=None,
           line_color=glow_color,
           line_width=3,
           line_alpha=alpha,
           line_cap="round",
           line_join="round")

# Add progress bar with gradient
progress_color = "#00C853"  # Slightly darker green for main bar
p.hbar(y=0, right='width', height=0.2, border_radius=19,
       source=source,
       fill_color=progress_color,
       line_color="#00E676",  # Lighter green for border
       line_width=2,
       line_cap="round",
       line_join="round")

# Add percentage text with glow effect
# Text shadow/glow layers
for dx, dy, alpha in [(0.02, 0.02, 0.1), (-0.02, -0.02, 0.1), (0.02, -0.02, 0.1), (-0.02, 0.02, 0.1)]:
    p.text(x='text_x', y=dy, text='text',
           source=source,
           text_align="center",
           text_baseline="middle",
           text_color=glow_color,
           text_font_size="20pt",
           text_font_style="bold",
           text_alpha=alpha)

# Main text
p.text(x='text_x', y=0, text='text',
       source=source,
       text_align="center",
       text_baseline="middle",
       text_color="#FFFFFF",
       text_font_size="20pt",
       text_font_style="bold")

# Create animation with easing
animation = CustomJS(args=dict(source=source, target_pct=TARGET_PERCENTAGE), code='''
    window.current_value = 0;
    window.target_value = parseFloat(target_pct);
    
    // Validate target value
    if (isNaN(window.target_value) || window.target_value < 0 || window.target_value > 100) {
        window.target_value = target_pct;
    }
    
    function easeOutCubic(x) {
        return 1 - Math.pow(1 - x, 3);
    }
    
    function updateProgress() {
        // Calculate the next value with easing
        const diff = window.target_value - window.current_value;
        const step = diff * 0.1;  // Adjust for animation speed
        
        if (Math.abs(diff) > 0.1) {
            window.current_value += step;
            
            // Ensure we don't exceed target value
            window.current_value = Math.min(window.current_value, window.target_value);
            
            // Calculate progress (0 to target percentage)
            const progress = window.current_value / 100;
            
            // Update progress bar
            source.data.width = [progress];
            source.data.text = [Math.round(window.current_value) + '%'];
            
            // Position text at the current width
            source.data.text_x = [progress/2];
            
            source.change.emit();
            
            // Continue animation
            setTimeout(updateProgress, 16);  // ~60fps
        }
    }
    
    updateProgress();
''')

# Add animation trigger
doc = curdoc()
doc.add_root(p)
doc.js_on_event('document_ready', animation)

# Show the plot
show(p)
