# https://discourse.bokeh.org/t/css-magic-custom-plot-effects/12491

from bokeh.models import Div, InlineStyleSheet
from bokeh.io import show
fancy_div_style = InlineStyleSheet(css="""
:host {
    position: relative;
    background: #21233a;
    color: #fff;
    border-radius: 12px;
    padding: 18px 28px;
    text-align: center;
    overflow: hidden;
    box-shadow: 0 6px 10px rgba(197, 153, 10, 0.2);
}
:host::after {
    content: '';
    position: absolute;
    top: 0; left: -80%; width: 200%; height: 100%;
    background: linear-gradient(120deg, transparent 40%, rgba(255, 255, 255, 0.355) 50%, transparent 60%);
    animation: shimmer 2.2s infinite;
    pointer-events: none;
    border-radius: inherit;
}
@keyframes shimmer {
    0%   { left: -80%; }
    100% { left: 100%; }
}
""")

merged_div = Div(
    text="""
    <img src="https://static.bokeh.org/branding/icons/bokeh-icon@5x.png" alt="Bokeh logo" style="width:120px; display:block; margin:auto; margin-bottom:20px;">
    <span style="display:block;color:deepskyblue;font-size:68px;font-weight:bold;letter-spacing:2px;">Bokeh</span>
    <span style="display:block;color:orange;font-size:30px;margin-top:-18px;"><i>Rocks</i></span>
    """,
    styles={'width': '420px', 'background-color': 'black', 'padding': '30px', 'border-radius': '22px', 'margin': '28px auto'},
    stylesheets=[fancy_div_style],
)

show(merged_div, title="Aether - Bokeh Div with Inline Stylesheet")
























from bokeh.plotting import figure, curdoc
from bokeh.models import Div, InlineStyleSheet
from bokeh.layouts import column
from bokeh.io import show
curdoc().theme = 'dark_minimal'
fancy_div_style = InlineStyleSheet(css="""
:host {
    position: relative;
    background: #444444;
    color: #fff;
    border-radius: 16px;
    padding: 18px 28px;
    text-align: center;
    overflow: hidden;
    box-shadow: 0 6px 18px red;
    margin: 28px auto;
}
:host > .bk-plot-wrapper {
    border-radius: 16px !important;
    overflow: hidden !important;
}
:host::after {
    content: '';
    position: absolute;
    top: 0; left: -80%; width: 200%; height: 100%;
    background: linear-gradient(120deg, transparent 40%, rgba(118, 244, 235, 0.22) 50%, transparent 60%);
    animation: shimmer 2.4s infinite;
    pointer-events: none;
    border-radius: inherit;
    z-index: 2;
}
@keyframes shimmer {
    0%   { left: -80%; }
    100% { left: 100%; }
}
""")

p = figure(border_fill_color="#444444", background_fill_color="#444444",
           )
p.line([1,2,3,4], [2,4,3,6], color="red", line_width=2)


layout = column(p, stylesheets=[fancy_div_style])
show(layout)


























from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models import InlineStyleSheet

pulse_shadow_css = InlineStyleSheet(css="""
:host {
    position: relative;
    background: #444444;
    border-radius: 20px;
    padding: 18px;
    margin: 40px auto;
    box-shadow:
        0 0 38px 10px rgba(255,70,0,0.46),
        0 0 70px 18px rgba(255,200,40,0.12),
        0 0 26px 5px rgba(255,235,90,0.22);
    width: 440px;
    height: 270px;
    box-sizing: border-box;
    z-index: 0;
    animation: pulse-shadow 2.2s infinite alternate;
}

@keyframes pulse-shadow {
    0% {
        box-shadow:
            0 0 16px 3px rgba(230, 70, 10, 0.90),
            0 0 32px 8px rgba(255, 185, 25, 0.60),
            0 0 10px 1px rgba(255, 240, 170, 0.82);
    }
    30% {
        box-shadow:
            0 0 32px 10px rgba(255, 130, 10, 0.82),
            0 0 44px 14px rgba(252, 200, 40, 0.40),
            0 0 22px 3px rgba(255, 235, 120, 0.62);
    }
    50% {
        box-shadow:
            0 0 42px 12px rgba(239, 110, 30, 0.98),
            0 0 70px 20px rgba(255, 208, 50, 0.23),
            0 0 32px 6px rgba(255, 245, 100, 0.79);
    }
    70% {
        box-shadow:
            0 0 60px 14px rgba(255, 162, 12, 0.83),
            0 0 90px 32px rgba(254, 200, 60, 0.22),
            0 0 38px 7px rgba(255, 246, 143, 0.61);
    }
    100% {
        box-shadow:
            0 0 80px 22px rgba(255, 80, 0, 0.78),
            0 0 120px 38px rgba(255, 220, 70, 0.15),
            0 0 60px 12px rgba(255, 248, 192, 0.53);
    }
}
""")

p = figure(
    title="Pulsing Fire Glow Shadow",
    border_fill_color="#444444", background_fill_color="#444444",
)
p.scatter([1,2,3,4], [2,4,3,6], color="deepskyblue", size=14)

container = column(
    p,
    stylesheets=[pulse_shadow_css],
    styles={'width': '640px', 'height': '470px', 'margin': '10 auto'}
)

show(container)
