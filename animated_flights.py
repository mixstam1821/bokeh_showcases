# https://discourse.bokeh.org/t/animated-flights/12629

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, WMTSTileSource
import numpy as np
import random

# Helper: WGS84 → Web Mercator (vectorized)
def wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi / 180.0)
    y = np.log(np.tan((90 + lat) * np.pi / 360.0)) * k
    return x, y

# Major global cities (optimized selection)
CITIES = {
    "New York": (-74.006, 40.7128),
    "Los Angeles": (-118.2437, 34.0522),
    "London": (-0.1276, 51.5074),
    "Paris": (2.3522, 48.8566),
    "Tokyo": (139.6917, 35.6895),
    "Dubai": (55.2708, 25.2048),
    "Singapore": (103.8198, 1.3521),
    "Sydney": (151.2093, -33.8688),
    "São Paulo": (-46.6333, -23.5505),
    "Mumbai": (72.8777, 19.0760),
    "Beijing": (116.4074, 39.9042),
    "Moscow": (37.6173, 55.7558),
    "Istanbul": (28.9784, 41.0082),
    "Bangkok": (100.5018, 13.7563),
    "Toronto": (-79.3832, 43.6532),
    "Hong Kong": (114.1694, 22.3193),
    "Shanghai": (121.4737, 31.2304),
    "Seoul": (126.9780, 37.5665),
    "Madrid": (-3.7038, 40.4168),
    "Rome": (12.4964, 41.9028),
    "Amsterdam": (4.9041, 52.3676),
    "Frankfurt": (8.6821, 50.1109),
    "Chicago": (-87.6298, 41.8781),
    "San Francisco": (-122.4194, 37.7749),
    "Miami": (-80.1918, 25.7617),
    "Delhi": (77.1025, 28.7041),
    "Mexico City": (-99.1332, 19.4326),
    "Cairo": (31.2357, 30.0444),
    "Johannesburg": (28.0473, -26.2041),
    "Melbourne": (144.9631, -37.8136)
}

# Optimized flight arc generation (reduced steps for performance)
def generate_flight_arc(lon1, lat1, lon2, lat2, steps=200):
    t = np.linspace(0, 1, steps)
    
    # Vectorized great circle interpolation
    lon_arc = lon1 + (lon2 - lon1) * t
    lat_arc = lat1 + (lat2 - lat1) * t
    
    # Altitude curve
    distance = np.sqrt((lon2 - lon1)**2 + (lat2 - lat1)**2)
    altitude_factor = min(distance * 0.7, 18)
    lat_arc += altitude_factor * np.sin(np.pi * t) * (1 - 0.3 * t)
    
    return wgs84_to_web_mercator(lon_arc, lat_arc)

# Create Bokeh figure
p = figure(
    x_range=(-2e7, 2e7), 
    y_range=(-1e7, 1e7),
    x_axis_type="mercator", 
    y_axis_type="mercator",
    width=1400, 
    height=800, 
    title="Live Global Flight Tracker",
)

# Dark map
dark_url = "https://basemaps.cartocdn.com/dark_all/{Z}/{X}/{Y}.png"
p.add_tile(WMTSTileSource(url=dark_url))

# Optimized styling
p.title.text_color = "#E0E0E0"
p.title.text_font_size = "18pt"
p.background_fill_color = "#0a0a0a"
p.border_fill_color = "#0a0a0a"
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

# Optimized parameters
N_FLIGHTS = 50
trail_length = 45

# Optimized color palette
FLIGHT_COLORS = [
    ("#00d4ff", "#0066ff"),
    ("#ff0080", "#ff6b00"),
    ("#00ff88", "#00cc66"),
    ("#ffdd00", "#ff8800"),
    ("#ff00ff", "#8800ff"),
    ("#00ffff", "#00aaff"),
]

# Pre-generate city list
city_list = list(CITIES.values())

# Storage for flights
flights = []

for _ in range(N_FLIGHTS):
    # Random route
    departure = random.choice(city_list)
    arrival = random.choice(city_list)
    while arrival == departure:
        arrival = random.choice(city_list)
    
    lon1, lat1 = departure
    lon2, lat2 = arrival
    
    x_arc, y_arc = generate_flight_arc(lon1, lat1, lon2, lat2)
    
    # Color scheme
    trail_color, glow_color = random.choice(FLIGHT_COLORS)
    
    # Data sources
    trail_src = ColumnDataSource(data=dict(x=[], y=[]))
    fade_src = ColumnDataSource(data=dict(x=[], y=[]))
    head_src = ColumnDataSource(data=dict(x=[], y=[]))
    
    # Optimized rendering - fewer layers
    # Outer glow
    p.line('x', 'y', source=trail_src, line_width=5,
           line_color=glow_color, line_alpha=0.18)
    
    # Core trail
    p.line('x', 'y', source=trail_src, line_width=2,
           line_color=trail_color, line_alpha=0.85)
    
    # Fade tail
    p.line('x', 'y', source=fade_src, line_width=1.5,
           line_color=trail_color, line_alpha=0.25)
    
    # Airplane head - optimized layers
    p.scatter('x', 'y', source=head_src, size=18, 
             color=glow_color, alpha=0.2)
    
    p.scatter('x', 'y', source=head_src, size=8, 
             color=trail_color, alpha=1.0)
    
    p.scatter('x', 'y', source=head_src, size=3, 
             color="white", alpha=1.0)
    
    # Store flight data
    flights.append({
        "x_arc": x_arc,
        "y_arc": y_arc,
        "trail_src": trail_src,
        "fade_src": fade_src,
        "head_src": head_src,
        "i": random.randint(0, len(x_arc) // 4),
        "speed": random.uniform(2.0, 4.0),  # speed
        "trail_color": trail_color,
        "glow_color": glow_color
    })

# Optimized update function
def update():
    for flight in flights:
        i = int(flight["i"])
        x_arc, y_arc = flight["x_arc"], flight["y_arc"]
        
        if i < len(x_arc):
            # Main trail
            start = max(0, i - trail_length)
            flight["trail_src"].data = dict(
                x=x_arc[start:i], 
                y=y_arc[start:i]
            )
            
            # Fading tail
            fade_start = max(0, i - trail_length * 2)
            flight["fade_src"].data = dict(
                x=x_arc[fade_start:start],
                y=y_arc[fade_start:start]
            )
            
            # Airplane position
            flight["head_src"].data = dict(
                x=[x_arc[i]], 
                y=[y_arc[i]]
            )
            
            # Smooth speed curve
            progress = i / len(x_arc)
            if progress < 0.15:  # Takeoff
                speed_factor = 0.6 + (progress / 0.15) * 0.4
            elif progress > 0.85:  # Landing
                speed_factor = 0.6 + ((1 - progress) / 0.15) * 0.4
            else:  # Cruise
                speed_factor = 1.0
            
            flight["i"] += flight["speed"] * speed_factor
        else:
            # Generate new route
            departure = random.choice(city_list)
            arrival = random.choice(city_list)
            while arrival == departure:
                arrival = random.choice(city_list)
            
            lon1, lat1 = departure
            lon2, lat2 = arrival
            
            flight["x_arc"], flight["y_arc"] = generate_flight_arc(lon1, lat1, lon2, lat2)
            flight["i"] = 0
            
            # 30% chance to change color
            if random.random() < 0.3:
                trail_color, glow_color = random.choice(FLIGHT_COLORS)
                flight["trail_color"] = trail_color
                flight["glow_color"] = glow_color

# Run at 30fps
curdoc().add_periodic_callback(update, 33)
curdoc().add_root(p)
