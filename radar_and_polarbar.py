# Check out my post here: https://discourse.bokeh.org/t/radar-and-polar-bar-plots/12255

# RADAR
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import (
    ColumnDataSource, HoverTool, PolarTransform, 
    Label, FixedTicker
)
from bokeh.palettes import Spectral6
from bokeh.io import output_file

# Generate sample data
n_variables = 8
n_series = 3
angles = np.linspace(0, 2*np.pi, n_variables, endpoint=False)
categories = [f'Variable {i+1}' for i in range(n_variables)]

# Generate random data
np.random.seed(42)
series_data = []
for _ in range(n_series):
    values = np.random.uniform(0.2, 1.0, n_variables)
    series_data.append(values)

# Close the polygons
angles_closed = np.append(angles, angles[0])
categories_closed = np.append(categories, categories[0])
series_data_closed = [np.append(series, series[0]) for series in series_data]

# Create polar transform
polar_transform = PolarTransform()

# Create figure
p = figure(
    width=600, height=600, 
    title="Advanced Radar Chart",
    x_range=(-1.7, 1.7), 
    y_range=(-1.7, 1.7),
    tools="pan,box_zoom,wheel_zoom,reset,save"
)

# Plot each series
colors = Spectral6[:n_series]
rr=[]

for i, (series, color) in enumerate(zip(series_data_closed, colors)):
    source = ColumnDataSource(data=dict(
        radius=series,
        angle=angles_closed,
        category=categories_closed,
        series=[f'Series {i+1}'] * len(series)
    ))
    
    # Use PolarTransform for plotting
    p.patch(x=polar_transform.x, 
            y=polar_transform.y,
            fill_color=colors[i],
            fill_alpha=0.2,
            line_color=colors[i],
            line_width=2,
            legend_label=f'Series {i+1}',
            source=source)
    
    
    rri = p.scatter(
        x=polar_transform.x, 
        y=polar_transform.y,
        size=8,
        color=color,
        source=source
    )
    rr.append(rri)

# Circular grid lines with PolarTransform
radii = np.linspace(0.2, 1.0, 5)
for radius in radii:
    # Create circular source
    theta = np.linspace(0, 2*np.pi, 100)
    circle_source = ColumnDataSource(data=dict(
        radius=[radius]*100,
        angle=theta
    ))
    
    # Plot circular grid lines
    p.line(
        x=polar_transform.x, 
        y=polar_transform.y,
        line_color="gray", 
        line_alpha=0.2,
        source=circle_source
    )
    
    # Add radius labels
    label_source = ColumnDataSource(data=dict(
        radius=[radius],
        angle=[3*np.pi/2],
        text=[f'{radius:.1f}']  # Add the text as a column
    ))
    
    p.text(
        x=polar_transform.x, 
        y=polar_transform.y,
        text='text',  # Reference the text column
        source=label_source,
        text_color="lime",
        text_alpha=0.6
    )
# Radial lines and category labels
for angle, category in zip(angles, categories):
    # Radial lines
    radial_source = ColumnDataSource(data=dict(
        radius=[0, 1],
        angle=[angle, angle]
    ))
    
    p.line(
        x=polar_transform.x, 
        y=polar_transform.y,
        line_color="gray", 
        line_alpha=0.2,
        source=radial_source
    )
    
    # Category labels
    label_source = ColumnDataSource(data=dict(
        radius=[1.3],
        angle=[angle],text = [category],
    ))
    
    p.text(
        x=polar_transform.x, 
        y=polar_transform.y,
        text='text',
        source=label_source,
        text_color="lime",
        text_align="center"
    )

# Hover tool
hover = HoverTool(
    
    renderers = rr,
    tooltips=[
    ('Series', '@series'),
    ('Category', '@category'),
    ('Value', '@radius{0.2f}')
])
p.add_tools(hover)

# Styling
p.title.text_color = "navy"
p.grid.grid_line_color = None
p.xaxis.visible = False
p.yaxis.visible = False
p.legend.click_policy = "hide"

output_file("polar_radar_chart_enhanced.html")
show(p)






# POLAR BAR
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Spectral6
import numpy as np
from math import pi

# Generate sample data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
values = np.random.randint(10, 100, 12)

# Calculate angles for each month
angles = [i*2*pi/12 for i in range(12)]
start_angles = [angle - pi/12 for angle in angles]
end_angles = [angle + pi/12 for angle in angles]

# Create ColumnDataSource
source = ColumnDataSource(data=dict(
    months=months,
    values=values,
    start_angles=start_angles,
    end_angles=end_angles,
    colors=Spectral6 * 2,  # Repeat colors to match number of months
    x=values * np.cos(angles),
    y=values * np.sin(angles)
))

# Create figure
p = figure(width=800, height=800, title="Polar Bar Chart",
          tools="pan,wheel_zoom,box_zoom,reset,save",
          x_range=(-150, 150), y_range=(-150, 150))

# Add wedges
wedges = p.wedge(x=0, y=0, radius='values',
                 start_angle='start_angles',
                 end_angle='end_angles',
                 fill_color='colors',
                 fill_alpha=0.7,
                 line_color="white",
                 source=source,
                 legend_field='months')

# Add hover tool
hover = HoverTool(renderers=[wedges],tooltips=[
    
    ('Month', '@months'),
    ('Value', '@values')
])
p.add_tools(hover)

# Add circular grid lines
for radius in np.linspace(0, 100, 11):
    circle = p.circle(x=0, y=0, radius=radius, fill_color=None,
                     line_color='gray', line_alpha=0.3)
    if radius > 0:
        label = p.text(x=[0], y=[radius], text=[f'{int(radius)}'],color="lime",
                      text_baseline="bottom", text_align="center")

# Add month labels at a fixed radius
label_radius = 110
x_labels = label_radius * np.cos(angles)
y_labels = label_radius * np.sin(angles)

label_source = ColumnDataSource(data=dict(
    x=x_labels,
    y=y_labels,
    months=months
))

labels = p.text(x='x', y='y', text='months',
               text_align='center', text_baseline='middle', color="grey",
               source=label_source)

# Customize the plot
p.grid.grid_line_color = None
p.axis.visible = False
p.outline_line_color = None

# Move legend to the right
p.legend.location = "right"
p.legend.click_policy = "hide"  # Allow toggling bars by clicking legend

# Output to file
output_file("polar_bar.html")
show(p)
