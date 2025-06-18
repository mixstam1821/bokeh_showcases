# see my post here for several examples: https://discourse.bokeh.org/t/custom-design-for-widgets/12479

from bokeh.io import show, curdoc
from bokeh.models import Slider, InlineStyleSheet
from bokeh.layouts import column

curdoc().theme = 'dark_minimal'

slider_style = InlineStyleSheet(css="""
/* Host: set the widget's container background */
:host {
  background: #16161e !important;   /* even darker than black for modern dark UI */
  border-radius: 12px !important;
  padding: 12px !important;
  box-shadow: 0 4px 12px #0006 !important;
}
/* Slider title */
:host .bk-slider-title {
  color: #00ffe0 !important;     /* bright cyan for the title */
  font-size: 1.2em !important;
  font-weight: bold !important;
  letter-spacing: 1px !important;
  font-family: 'Fira Code', 'Consolas', 'Menlo', monospace !important;
  margin-bottom: 14px !important;
  text-shadow: 0 2px 12px #00ffe099;
}
/* Track (background) */
:host .noUi-base, :host .noUi-target {
  background: #23233c !important;
    border: 1px solid #2a3132 !important;

}
/* Filled portion */
:host .noUi-connect {
  background: linear-gradient(90deg, #00ffe0 10%, #d810f7 90%) !important;
  box-shadow: 0 0 12px #00ffe099;
  border-radius: 12px !important;
}
/* Handle */
:host .noUi-handle {
  background: #343838 !important;
  border: 2px solid #00ffe0 !important;
  border-radius: 50%;
  width: 20px;
  height: 20px;
}
/* Handle hover/focus */
:host .noUi-handle:hover, :host .noUi-handle:focus {
  border-color: #ff2a68 !important;
  box-shadow: 0 0 10px #ff2a6890;
}
/* Tooltip */
:host .noUi-tooltip {
  background: #343838 !important;
  color: #00ffe0 !important;
  font-family: 'Consolas', monospace;
  border-radius: 6px;
  border: 1px solid #00ffe0;
}
""")

slider = Slider(
    start=0, end=100, value=42, step=1, 
    title="💠 Custom Neon Slider", width=350, stylesheets=[slider_style]
)

show(column(slider))
