# https://discourse.bokeh.org/t/custom-design-for-widgets/12479/2
from bokeh.io import curdoc
from bokeh.models import TabPanel, Tabs, ColumnDataSource, InlineStyleSheet
from bokeh.plotting import figure
from bokeh.layouts import column
import numpy as np
import pandas as pd
curdoc().theme = 'dark_minimal'
# --- Data setup ---
N = 100
dates = pd.date_range("2016-01-01", periods=N, freq="M")
signal = 5 + 2*np.sin(2*np.pi*(dates.month-1)/12) + np.random.normal(0, 0.7, N)
df = pd.DataFrame({'value': signal}, index=dates)
monthly_means = df.groupby(df.index.month)['value'].transform('mean')
anomalies = df['value'] - monthly_means

source = ColumnDataSource(data=dict(time=dates, value=signal, anomaly=anomalies))

# --- Time Series plot ---
p1 = figure(width=800, height=350, x_axis_type="datetime", title="Time Series", border_fill_color="#2d2d2d")
p1.line('time', 'value', source=source, line_width=2, color="#0af", legend_label="Raw")
p1.legend.location = "top_left"
p1.xaxis.axis_label = "Time"
p1.yaxis.axis_label = "Value"

# --- Anomalies plot ---
p2 = figure(width=800, height=350, x_axis_type="datetime", title="Deseasonalized Anomalies", border_fill_color="#2d2d2d")
p2.line('time', 'anomaly', source=source, line_width=2, color="#e44", legend_label="Deseasonalized")
p2.legend.location = "top_left"
p2.xaxis.axis_label = "Time"
p2.yaxis.axis_label = "Anomaly"

# --- Your InlineStyleSheet for beautiful tabs ---
tabs_style = InlineStyleSheet(css="""
/* Main tabs container */
:host {
    background: #2d2d2d !important;
    border-radius: 14px !important;
    padding: 8px !important;
    margin: 10px !important;
    box-shadow: 0 6px 20px #00ffe055, 0 2px 10px rgba(0, 0, 0, 0.3) !important;
    border: 1px solid rgba(0, 191, 255, 0.3) !important;
}
/* Tab navigation bar */
:host .bk-tabs-header {
    background: transparent !important;
    border-bottom: 2px solid #00bfff !important;
    margin-bottom: 8px !important;
}
/* Individual tab buttons */
:host .bk-tab {
    background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%) !important;
    color: #00bfff !important;
    border: 1px solid #555 !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 12px 20px !important;
    margin-right: 4px !important;
    font-family: 'Arial', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95em !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}
/* Tab hover effect */
:host .bk-tab:hover {
    background: linear-gradient(135deg, #dc1cdd 0%, #ff1493 100%) !important;
    color: #ffffff !important;
    border-color: #dc1cdd !important;
    box-shadow: 0 4px 15px rgba(220, 28, 221, 0.5) !important;
    transform: translateY(-2px) !important;
}
/* Active tab styling */
:host .bk-tab.bk-active {
    background: linear-gradient(135deg, #00bfff 0%, #0080ff 100%) !important;
    color: #000000 !important;
    border-color: #00bfff !important;
    box-shadow: 0 4px 20px rgba(0, 191, 255, 0.6), inset 0 2px 0 rgba(255, 255, 255, 0.3) !important;
    transform: translateY(-1px) !important;
    font-weight: 700 !important;
}
/* Active tab glow effect */
:host .bk-tab.bk-active::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%) !important;
    animation: shimmer 2s infinite !important;
}
@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
/* Tab content area */
:host .bk-tab-content {
    background: transparent !important;
    padding: 16px !important;
    border-radius: 0 0 10px 10px !important;
}
/* Focus states for accessibility */
:host .bk-tab:focus {
    outline: 2px solid #00bfff !important;
    outline-offset: 2px !important;
}
/* Disabled tab state */
:host .bk-tab:disabled {
    background: #1a1a1a !important;
    color: #666 !important;
    cursor: not-allowed !important;
    opacity: 0.5 !important;
}
""")

# --- Panels and Tabs ---
tabs = Tabs(tabs=[
    TabPanel(child=column(p1), title="Timeseries"),
    TabPanel(child=column(p2), title="Anomalies"),
], stylesheets=[tabs_style], styles={'width':'890px'},)

curdoc().add_root(tabs)
