# see also here my post: https://discourse.bokeh.org/t/ripple-effect/12235
######################################
#            First Example           #
######################################


from bokeh.plotting import figure, show, curdoc
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, HoverTool, CustomJS
from bokeh.palettes import Plasma256
from bokeh.events import DocumentReady
import numpy as np

# Generate sample data for cities
np.random.seed(42)

# Generate cities around the world (avoiding oceans for visibility)
cities = [
    ("New York", 40.7128, -74.0060),
    ("London", 51.5074, -0.1278),
    ("Tokyo", 35.6762, 139.6503),
    ("Paris", 48.8566, 2.3522),
    ("Beijing", 39.9042, 116.4074),
    ("Moscow", 55.7558, 37.6173),
    ("Dubai", 25.2048, 55.2708),
    ("Singapore", 1.3521, 103.8198),
    ("Sydney", -33.8688, 151.2093),
    ("Rio de Janeiro", -22.9068, -43.1729),
    ("Cairo", 30.0444, 31.2357),
    ("Mumbai", 19.0760, 72.8777),
    ("Los Angeles", 34.0522, -118.2437),
    ("Berlin", 52.5200, 13.4050),
    ("Toronto", 43.6532, -79.3832)
]

# Convert to Web Mercator coordinates
def convert_to_mercator(lons, lats):
    """Convert longitude/latitude to Web Mercator coordinates"""
    k = 6378137
    x = np.array(lons) * (k * np.pi/180.0)
    y = np.log(np.tan((90 + np.array(lats)) * np.pi/360.0)) * k
    return x, y

city_names = [city[0] for city in cities]
city_lats = [city[1] for city in cities]
city_lons = [city[2] for city in cities]
city_x, city_y = convert_to_mercator(city_lons, city_lats)
base_sizes = np.random.uniform(10, 20, len(cities))
city_colors = np.random.choice(Plasma256, len(cities))

# Create the figure with web mercator coordinates
p = figure(width=800, height=600,
          x_range=(-18000000, 18000000), y_range=(-6000000, 8000000),
          x_axis_type="mercator", y_axis_type="mercator",
          title="Animated World Cities",
          background_fill_color='#252525',
          border_fill_color='#252525',
          outline_line_color=None)

# Add the tile source (CartoDB Dark Matter)
p.add_tile("CartoDB Dark Matter", retina=True)

# Create sources for different glow layers
glow_sources = []
n_glows = 4
for i in range(n_glows):
    source = ColumnDataSource({
        'name': city_names,
        'lat': city_lats,
        'lon': city_lons,
        'x': city_x,
        'y': city_y,
        'size': [s * (i + 1) for s in base_sizes],
        'color': city_colors,
        'alpha': [0.1] * len(cities)
    })
    glow_sources.append(source)

# Main city source
city_source = ColumnDataSource({
    'name': city_names,
    'lat': city_lats,
    'lon': city_lons,
    'x': city_x,
    'y': city_y,
    'size': base_sizes,
    'color': city_colors,
    'alpha': [1.0] * len(cities)
})

# Add glow layers
glow_renderers = []
for source in glow_sources:
    glow = p.circle('x', 'y',
                   size='size',
                   fill_color='color',
                   line_color=None,
                   alpha='alpha',
                   source=source)
    glow_renderers.append(glow)

# Add main city points
main_renderer = p.circle('x', 'y',
                        size='size',
                        fill_color='color',
                        line_color='white',
                        line_width=1,
                        alpha='alpha',
                        source=city_source)

# Create animation callback
animation = CustomJS(args=dict(sources=glow_sources, main_source=city_source), code="""
    let t = 0;
    const n_cities = main_source.data.size.length;
    
    function animate() {
        // Update each glow layer
        sources.forEach((source, i) => {
            const phase = 2 * Math.PI * i / sources.length;
            const alphas = new Array(n_cities).fill(0);
            
            for (let j = 0; j < n_cities; j++) {
                // Create slightly different frequencies for each city
                const freq = 1 + j * 0.1;
                alphas[j] = 0.3 * (1 + Math.sin(freq * t + phase)) / 2;
            }
            
            source.data.alpha = alphas;
            source.change.emit();
        });
        
        // Pulse the main points slightly
        const main_alphas = new Array(n_cities).fill(0);
        for (let j = 0; j < n_cities; j++) {
            const freq = 1 + j * 0.1;
            main_alphas[j] = 0.7 + 0.3 * Math.sin(freq * t) / 2;
        }
        main_source.data.alpha = main_alphas;
        main_source.change.emit();
        
        t += 0.05;
        requestAnimationFrame(animate);
    }
    
    animate();
""")

# Add hover tool for cities
hover = HoverTool(tooltips=[
    ('City', '@name'),
    ('Latitude', '@lat{0.00}°'),
    ('Longitude', '@lon{0.00}°')
])
p.add_tools(hover)

# Customize the plot
p.grid.grid_line_color = None
p.axis.visible = False

# Style the title
p.title.text_color = "white"
p.title.text_font_size = "16px"
p.title.align = "center"

# Add zoom tools
p.toolbar.active_scroll = p.select_one('WheelZoomTool')

# Add plot to document and trigger animation
doc = curdoc()
doc.add_root(p)
doc.js_on_event(DocumentReady, animation)

# Output to file
output_file("geo_plot_animated_doc.html")
show(p)



######################################
#           Second Example           #
######################################



from bokeh.plotting import figure
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.io import curdoc
import numpy as np

# Generate scatter points
np.random.seed(42)
N = 30  # Number of points
x = np.random.normal(0, 1, N)
y = np.random.normal(0, 1, N)

# Create circles (3 per point)
n_circles = 4
x_ripple = np.repeat(x, n_circles)
y_ripple = np.repeat(y, n_circles)
base_sizes = [10 + i * 8 for i in range(n_circles)] * N

# Create data source
source = ColumnDataSource(data=dict(
    x=x_ripple,
    y=y_ripple,
    size=base_sizes
))

# Create data source
source2 = ColumnDataSource(data=dict(
    x=x_ripple,
    y=y_ripple,
    size=[i/4 for i in base_sizes]
))
# Create plot
p = figure(title="Animated Circles",
           x_axis_label='X Axis',
           y_axis_label='Y Axis',
           width=800,
           height=600,
           tools="pan,box_zoom,reset,save")

# Add circles
circles = p.circle('x', 'y',
                  size='size',
                  fill_color='orange',
                  line_color='orange',
                  fill_alpha=0,
                  line_alpha=1,line_width=1,
                  source=source)



# source2=source
# Add circles
circles2 = p.circle('x', 'y',
                  size='size',
                  fill_color='orange',
                  line_color='orange',
                  fill_alpha=1,
                  line_alpha=1,
                  source=source2)

p.circle(x = [-2,-1.4,-0.5,0.9,1,2.3],y = [0,1,2,-1,-2,-0.5], fill_color = 'lime',size = 20)
# Create animation callback
animation = CustomJS(args=dict(source=source, base_sizes=base_sizes), code='''
    let frame = 0;
    const data = source.data;
    const sizes = data['size'];
    
    function animate() {
        // Update sizes with sine wave
        for (let i = 0; i < sizes.length; i++) {
            const baseSize = base_sizes[i];
            sizes[i] = baseSize * (1 + 0.5 * Math.sin(frame + i * 0.5));
        }
        
        // Update frame and data source
        frame += 0.1;
        source.change.emit();
        
        // Request next frame
        setTimeout(animate, 50);
    }
    
    // Start animation
    animate();
''')

# Add plot to document and trigger animation
doc = curdoc()
doc.add_root(p)
doc.js_on_event('document_ready', animation)

# Show the plot
show(p)
