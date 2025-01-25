# see also my post here: https://discourse.bokeh.org/t/initial-animation-with-custom-easing/12248

# line
from bokeh.plotting import figure, show
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.io import curdoc
import numpy as np

# Generate some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a ColumnDataSource with initial empty data
source = ColumnDataSource(data=dict(x=[], y=[]))

# Create a new plot with a title and axis labels
p = figure(title="Animated Line Plot with Bounce", x_axis_label='x', y_axis_label='y',
           x_range=(0, 10), y_range=(-1.5, 1.5))

# Add a line renderer with legend and gradient effect
line = p.line('x', 'y', source=source, legend_label="sin(x)", 
              line_width=3, line_color='#FF4081')  # Hot pink color for bounce effect
p.legend.click_policy = "hide"

# Create animation callback with bounce easing
animation = CustomJS(args=dict(source=source, x=x.tolist(), y=y.tolist()), code='''
    let counter = 0;
    const step = 2;  // Smaller step for smoother animation
    const total_points = x.length;
    
    function bounceOut(t) {
        const n1 = 7.5625;
        const d1 = 2.75;
        
        if (t < 1 / d1) {
            return n1 * t * t;
        } else if (t < 2 / d1) {
            t -= 1.5 / d1;
            return n1 * t * t + 0.75;
        } else if (t < 2.5 / d1) {
            t -= 2.25 / d1;
            return n1 * t * t + 0.9375;
        } else {
            t -= 2.625 / d1;
            return n1 * t * t + 0.984375;
        }
    }
    
    function frame() {
        if (counter < total_points) {
            const data = source.data;
            
            // Use bounce easing for the counter
            const progress = counter / total_points;
            const bounced_progress = bounceOut(progress);
            const current_length = Math.floor(bounced_progress * total_points);
            
            // Update data with bounced length
            data['x'] = x.slice(0, current_length);
            data['y'] = y.slice(0, current_length);
            source.change.emit();
            
            if (counter < total_points) {
                // Dynamic timing for bounce effect
                const delay = 20 + (10 * Math.sin(progress * Math.PI));  // Faster overall with slight variation
                counter += step;
                setTimeout(frame, delay);
            }
        }
    }
    
    frame();
''')

# Add plot to document and trigger animation
doc = curdoc()
doc.add_root(p)
doc.js_on_event('document_ready', animation)

# Show the plot
show(p)




# bars
from bokeh.plotting import figure, show
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.layouts import row
from bokeh.io import curdoc
import numpy as np

# Generate some sample data
x = list(range(8))
y = [4, 7, 3, 9, 2, 6, 5, 8]

# Create data sources
source = ColumnDataSource(data=dict(x=x, top=[0]*8))

# Create figure
p = figure(title="Animated Bar Plot", x_range=(-0.5, 7.5), y_range=(0, 10))

# Add bar renderer
bars = p.vbar(x='x', top='top', source=source, width=0.8,
              fill_color='#2196F3', line_color=None)

# Create animation callback
animation = CustomJS(args=dict(source=source, final_y=y), code='''
    let counter = 0;
    const total_frames = 60;
    
    function bounceOut(t) {
        const n1 = 7.5625;
        const d1 = 2.75;
        
        if (t < 1 / d1) {
            return n1 * t * t;
        } else if (t < 2 / d1) {
            t -= 1.5 / d1;
            return n1 * t * t + 0.75;
        } else if (t < 2.5 / d1) {
            t -= 2.25 / d1;
            return n1 * t * t + 0.9375;
        } else {
            t -= 2.625 / d1;
            return n1 * t * t + 0.984375;
        }
    }
    
    function frame() {
        if (counter <= total_frames) {
            const progress = counter / total_frames;
            const data = source.data;
            
            // Animate each bar with bounce easing
            const bounced = bounceOut(progress);
            data.top = final_y.map(y => y * bounced);
            
            source.change.emit();
            
            if (counter < total_frames) {
                counter++;
                setTimeout(frame, 20);
            }
        }
    }
    
    frame();
''')

# Add plot to document and trigger animation
doc = curdoc()
doc.add_root(p)
doc.js_on_event('document_ready', animation)

# Show the plot
show(p)
