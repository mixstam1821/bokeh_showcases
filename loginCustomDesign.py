#https://discourse.bokeh.org/t/login-with-custom-design/12464
# loginapp.py
from bokeh.io import curdoc
from bokeh.events import DocumentReady
from bokeh.models import TextInput, PasswordInput, Button, Div, InlineStyleSheet,GlobalInlineStyleSheet, Div,ColumnDataSource,CustomJS
from bokeh.plotting import figure
from bokeh.layouts import column,row, Spacer
import pandas as pd
import numpy as np
gstyle = GlobalInlineStyleSheet(css=""" html, body, .bk, .bk-root { margin: 0; padding: 0; height: 100%; color: white; font-family: 'Consolas', 'Courier New', monospace; } .bk { color: white; } .bk-input, .bk-btn, .bk-select, .bk-slider-title, .bk-headers, .bk-label, .bk-title, .bk-legend, .bk-axis-label { color: white !important; } .bk-input::placeholder { color: #aaaaaa !important; } """)
style = InlineStyleSheet(css=""" .bk-btn { background-color: #00ffe0; color: #1e1e2e; font-weight: bold; border: 10px solid #00ffe0; border-radius: 6px; transform: rotate(0deg); box-shadow: none; transition: all 0.3s ease-in-out; } /* 🟦 Hover: #1e1e2e + rotate */ .bk-btn:hover { background-color: #1e1e2e; border-color: #1e1e2e; color: #00ffe0; transform: rotate(3deg); box-shadow: 0 0 15px 3px #00ffe0; } /* 🔴 Active (click hold): red + stronger rotate */ .bk-btn:active { background-color: red; border-color: red; transform: rotate(6deg); box-shadow: 0 0 15px 3px red; } """)
style2 = InlineStyleSheet(css=""" .bk-input { background-color: #1e1e1e; color: #d4d4d4; font-weight: 500; border: 1px solid #3c3c3c; border-radius: 5px; padding: 6px 10px; font-family: 'Consolas', 'Courier New', monospace; transition: all 0.2s ease; } /* Input Hover */ .bk-input:hover { width: 250px; height: 45px; background-color: #1e1e1e; color: #d4d4d4; font-weight: 500; border: 1px solid #3c3c3c; border-radius: 5px; padding: 6px 10px; font-family: 'Consolas', 'Courier New', monospace; transition: all 0.2s ease; } /* Input Focus */ .bk-input:focus { background-color: #1e1e1e; color: #d4d4d4; font-weight: 500; border: 1px solid #3c3c3c; border-radius: 5px; padding: 6px 10px; font-family: 'Consolas', 'Courier New', monospace; transition: all 0.2s ease; } .bk-input:active { outline: none; background-color: #1e1e1e; color: #d4d4d4; font-weight: 500; border: 1px solid #3c3c3c; border-radius: 5px; padding: 6px 10px; font-family: 'Consolas', 'Courier New', monospace; transition: all 0.2s ease; } .bk-input:-webkit-autofill { background-color: #1e1e1e !important; color: #d4d4d4 !important; -webkit-box-shadow: 0 0 0px 1000px #1e1e1e inset !important; -webkit-text-fill-color: #d4d4d4 !important; } """)

# 🔐 Credentials
VALID_USERS = {"admin": "1234", "michael": "secretpass"}

# 🎛️ UI Inputs
username_input = TextInput(title="Username", stylesheets=[style2])
password_input = PasswordInput(title="Password", stylesheets=[style2])
login_button = Button(label="Login", button_type="success", width=220,stylesheets=[style],)
status = Div(text="🔐 Please log in")

# 🔀 Initial login layout
login_layout = column(username_input, password_input, login_button, status,stylesheets=[gstyle])

# ─── DATA ─────────────────────────────────────────────
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
values = np.cumsum(np.random.randn(100))
noise = np.random.randn(100)
categories = ["Apples", "Bananas", "Cherries", "Dates"]
counts = np.random.randint(10, 100, size=4)

# ─── SOURCES ──────────────────────────────────────────
line_src = ColumnDataSource(data=dict(x=dates, y=values))
scatter_src = ColumnDataSource(data=dict(x=values, y=noise))
bar_src = ColumnDataSource(data=dict(x=categories, top=counts))

# ─── PLOTS ────────────────────────────────────────────
line_plot = figure(title="📈 Time Series Line Plot", x_axis_type="datetime", height=300, width=800, background_fill_color=None, border_fill_color=None,)
line_plot.line("x", "y", source=line_src, line_width=3, color="deepskyblue")
line_plot.grid.visible = False;line_plot.xaxis.major_label_text_color = "white";line_plot.yaxis.major_label_text_color = "white"

scatter_plot = figure(title="✴️ Scatter Plot", height=300, width=800, background_fill_color=None, border_fill_color=None,)
scatter_plot.circle("x", "y", source=scatter_src, size=8, color="orange", alpha=0.7)
scatter_plot.grid.visible = False;scatter_plot.xaxis.major_label_text_color = "white";scatter_plot.yaxis.major_label_text_color = "white"

bar_plot = figure(title="📊 Bar Chart", x_range=categories, height=300, width=800, background_fill_color=None, border_fill_color=None,)
bar_plot.vbar(x="x", top="top", source=bar_src, width=0.6, color="limegreen")
bar_plot.grid.visible = False;bar_plot.xaxis.major_label_text_color = "white";bar_plot.yaxis.major_label_text_color = "white"

source = ColumnDataSource(data=dict(x=[1, 2, 3, 4], y=[3, 7, 2, 6]))
plot = figure(title="Private Dashboard", width=800, height=400, background_fill_color=None,border_fill_color=None,)
plot.line(x='x', y='y', source=source, line_width=3, color="deepskyblue")
plot.xaxis.visible = False;plot.yaxis.visible = False;plot.grid.visible = False;plot.outline_line_color = None

# ─── TEXT DIVS ────────────────────────────────────────
intro = Div(text="""
<h1 style='color:#00ffe0'>🚀 Interactive Bokeh Dashboard</h1>
<p>This demo includes a timeseries line chart, a scatter plot, and a bar chart, all with animated particles in the background.</p>
""", width=800)

mid_text = Div(text="<h2>📌 Correlation View</h2><p>Plotting values vs noise.</p>", width=800)
bottom_text = Div(text="<h2>🍉 Category Overview</h2><p>Simple bar plot for fake categories.</p>", width=800)

# ─── FINAL LAYOUT ─────────────────────────────────────
layout = column( row(column(intro, Spacer(height=20), line_plot), Spacer(height=40), column(mid_text, scatter_plot, Spacer(height=40))), bottom_text, bar_plot, stylesheets=[gstyle] )

# 🎉 Post-login layout
plot_layout = column(Div(text="<h2 style='color:white;'>🎉 Welcome!</h2>"), plot,layout,stylesheets=[gstyle])

# 🔐 Auth logic
def login_callback():
    user = username_input.value.strip()
    pw = password_input.value.strip()
    if VALID_USERS.get(user) == pw:
        curdoc().clear()
        curdoc().add_root(plot_layout)
    else:
        status.text = "❌ Invalid username or password."

login_button.on_click(login_callback)

# 🧪 JS Background Particles
particles_js = """ (function() { if (window.particlesLoaded) return; window.particlesLoaded = true; const container = document.createElement("div"); container.id = "particles-js"; Object.assign(container.style, { position: "fixed", top: "0", left: "0", width: "100%", height: "100%", zIndex: "-1", pointerEvents: "none", backgroundColor: "#0f0f0f" }); document.body.appendChild(container); const script = document.createElement("script"); script.src = "https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"; script.onload = function() { particlesJS("particles-js", { particles: { number: { value: 160 }, color: { value: "#00ffe0" }, shape: { type: "circle" }, opacity: { value: 0.4 }, size: { value: 2 }, line_linked: { enable: true, distance: 140, color: "#00ffe0", opacity: 0.4, width: 1 }, move: { enable: true, speed: 1.6, direction: "none", out_mode: "out" } }, interactivity: { events: { onhover: { enable: true, mode: "repulse" } }, modes: { repulse: { distance: 100 } } }, retina_detect: true }); }; document.head.appendChild(script); })(); """

curdoc().js_on_event(DocumentReady, CustomJS(code=particles_js))

# 🔰 Start with login layout
curdoc().add_root(column(login_layout,    styles={ "display": "flex", "justify-content": "center", "align-items": "center", "height": "100vh", "width": "100vw", "background-color": "transparent",},))
