# my post: https://discourse.bokeh.org/t/laser-beam-with-joystick/12556
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Div, InlineStyleSheet
from bokeh.events import Pan, PanEnd
from bokeh.layouts import column
import numpy as np
import time

# --- Game timing ---
start_time = time.time()
game_duration = 10  # seconds

# --- Joystick setup ---
center_x, center_y = 0, 0
radius_limit = 1.0

# Data sources
knob_source = ColumnDataSource(data=dict(x=[center_x], y=[center_y]))
shaft_source = ColumnDataSource(data=dict(xs=[[center_x, center_x]], ys=[[center_y, center_y]]))

# Beam layers for glow effect
beam_core = ColumnDataSource(data=dict(xs=[[]], ys=[[]]))
beam_glow1 = ColumnDataSource(data=dict(xs=[[]], ys=[[]]))
beam_glow2 = ColumnDataSource(data=dict(xs=[[]], ys=[[]]))

# Targets (scatter points) + respawn timer
np.random.seed(42)
target_x = np.random.uniform(-10, 10, 8)
target_y = np.random.uniform(-10, 10, 8)
target_colors = ["red"] * len(target_x)
last_hit_time = [None] * len(target_x)
respawn_delay = 3  # seconds before respawn

targets_source = ColumnDataSource(data=dict(x=target_x, y=target_y, color=target_colors))

# Joystick base
theta = np.linspace(0, 2*np.pi, 200)
base_source_outer = ColumnDataSource(data=dict(x=radius_limit*np.cos(theta),
                                               y=radius_limit*np.sin(theta)))
base_source_inner = ColumnDataSource(data=dict(x=(radius_limit*0.8)*np.cos(theta),
                                               y=(radius_limit*0.8)*np.sin(theta)))

# Figure
p = figure(width=900, height=900, x_range=(-15, 15), y_range=(-15, 15),
           match_aspect=True, tools="", toolbar_location=None,
           background_fill_color="#000")
p.axis.visible = False
p.grid.visible = False

# --- Joystick visuals ---
p.patch('x', 'y', source=base_source_outer, fill_color="#003300", alpha=0.8, line_color=None)
p.patch('x', 'y', source=base_source_inner, fill_color="#111111", alpha=1.0, line_color=None)
p.line('x', 'y', source=base_source_outer, line_color="lime", line_width=3, alpha=0.7)
p.multi_line(xs='xs', ys='ys', source=shaft_source, line_color="gray", line_width=6, alpha=0.9)
p.circle('x', 'y', source=knob_source, size=80, fill_color="lime", fill_alpha=1,
         line_color="silver", line_width=4)
p.circle('x', 'y', source=knob_source, size=60, fill_color="lime", fill_alpha=1,
         line_color="lime", line_width=2)
p.circle('x', 'y', source=knob_source, size=30, fill_color="lime", fill_alpha=1,
         line_color="lime", line_width=1)

# --- Targets ---
p.circle('x', 'y', source=targets_source, size=15, fill_color='color', line_color="black", line_width=2)

# --- Laser beam with glow ---
p.multi_line(xs='xs', ys='ys', source=beam_glow2, line_color="lime", line_width=15, alpha=0.2)
p.multi_line(xs='xs', ys='ys', source=beam_glow1, line_color="lime", line_width=10, alpha=0.3)
p.multi_line(xs='xs', ys='ys', source=beam_core, line_color="lime", line_width=5, alpha=0.9)

# --- Win message ---
pulse_shadow_css = InlineStyleSheet(css=""" :host { position: absolute; background: #444444; border-radius: 20px; padding: 18px; margin: 10px auto; box-shadow: 0 0 38px 10px rgba(255,70,0,0.46), 0 0 70px 18px rgba(255,200,40,0.12), 0 0 26px 5px rgba(255,235,90,0.22); width: 440px; height: 170px; box-sizing: border-box; z-index: 0; animation: pulse-shadow 1.2s infinite alternate; } @keyframes pulse-shadow { 0% { box-shadow: 0 0 16px 3px rgba(230, 70, 10, 0.90), 0 0 32px 8px rgba(255, 185, 25, 0.60), 0 0 10px 1px rgba(255, 240, 170, 0.82); } 30% { box-shadow: 0 0 32px 10px rgba(255, 130, 10, 0.82), 0 0 44px 14px rgba(252, 200, 40, 0.40), 0 0 22px 3px rgba(255, 235, 120, 0.62); } 50% { box-shadow: 0 0 42px 12px rgba(239, 110, 30, 0.98), 0 0 70px 20px rgba(255, 208, 50, 0.23), 0 0 32px 6px rgba(255, 245, 100, 0.79); } 70% { box-shadow: 0 0 60px 14px rgba(255, 162, 12, 0.83), 0 0 90px 32px rgba(254, 200, 60, 0.22), 0 0 38px 7px rgba(255, 246, 143, 0.61); } 100% { box-shadow: 0 0 80px 22px rgba(255, 80, 0, 0.78), 0 0 120px 38px rgba(255, 220, 70, 0.15), 0 0 60px 12px rgba(255, 248, 192, 0.53); } } """)

win_message = Div(text="", stylesheets=[pulse_shadow_css],styles={"color": "lime", "font-size": "30px", "text-align": "center"})

# --- Event handling ---
def on_pan(event):
    dx = event.x - center_x
    dy = event.y - center_y
    dist = np.sqrt(dx**2 + dy**2)
    if dist > radius_limit:
        dx = dx / dist * radius_limit
        dy = dy / dist * radius_limit
        dist = radius_limit

    knob_source.data = dict(x=[center_x + dx], y=[center_y + dy])
    shaft_source.data = dict(xs=[[center_x, center_x + dx]], ys=[[center_y, center_y + dy]])

    beam_len = 400 * (dist / radius_limit)
    if dist > 0:
        bx = [center_x, center_x + beam_len * (dx / dist)]
        by = [center_y, center_y + beam_len * (dy / dist)]
    else:
        bx, by = [], []

    beam_core.data = dict(xs=[bx], ys=[by])
    beam_glow1.data = dict(xs=[bx], ys=[by])
    beam_glow2.data = dict(xs=[bx], ys=[by])

    # --- Collision detection ---
    if dist > 0:
        beam_angle = np.arctan2(dy, dx)
        max_range = beam_len
        angle_tolerance = np.deg2rad(5)  # 5 degrees

        tx, ty = np.array(targets_source.data['x']), np.array(targets_source.data['y'])
        colors = list(targets_source.data['color'])

        for i in range(len(tx)):
            target_angle = np.arctan2(ty[i] - center_y, tx[i] - center_x)
            target_dist = np.sqrt((tx[i] - center_x)**2 + (ty[i] - center_y)**2)
            angle_diff = np.abs((beam_angle - target_angle + np.pi) % (2*np.pi) - np.pi)

            if colors[i] != "#000" and target_dist <= max_range and angle_diff < angle_tolerance:
                colors[i] = "#000"
                last_hit_time[i] = time.time()

        targets_source.data['color'] = colors

def on_pan_end(event):
    knob_source.data = dict(x=[center_x], y=[center_y])
    shaft_source.data = dict(xs=[[center_x, center_x]], ys=[[center_y, center_y]])
    beam_core.data = dict(xs=[[]], ys=[[]])
    beam_glow1.data = dict(xs=[[]], ys=[[]])
    beam_glow2.data = dict(xs=[[]], ys=[[]])

# --- Respawn logic ---
def respawn_targets():
    tx, ty, colors = list(targets_source.data['x']), list(targets_source.data['y']), list(targets_source.data['color'])
    now = time.time()

    for i in range(len(colors)):
        if colors[i] == "#000" and last_hit_time[i] is not None:
            if now - last_hit_time[i] >= respawn_delay:
                tx[i] = np.random.uniform(-10, 10)
                ty[i] = np.random.uniform(-10, 10)
                colors[i] = "red"
                last_hit_time[i] = None

    targets_source.data = dict(x=tx, y=ty, color=colors)

# --- Game timer ---
def check_game_timer():
    elapsed = time.time() - start_time
    if elapsed >= game_duration:
        # Stop everything and show win message
        curdoc().remove_periodic_callback(respawn_cb)
        curdoc().remove_periodic_callback(timer_cb)
        curdoc().clear()
        curdoc().add_root(win_message)
        win_message.text = "🎉 Congrats!🎉 <br>🎉 Bokeh Rocks! 🎉"

p.on_event(Pan, on_pan)
p.on_event(PanEnd, on_pan_end)

respawn_cb = curdoc().add_periodic_callback(respawn_targets, 200)
timer_cb = curdoc().add_periodic_callback(check_game_timer, 200)

curdoc().add_root(column(p))
curdoc().title = "Joystick Laser Game"
