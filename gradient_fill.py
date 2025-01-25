# https://discourse.bokeh.org/t/gradient-fill-color/12252
from bokeh.plotting import figure, show
from bokeh.io import curdoc
from bokeh.models import HoverTool,ImageURLTexture
curdoc().theme = 'dark_minimal'

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]

hover = HoverTool(
    tooltips = [
        ("val", "@values"),
        ("(x,y)", "($x{int}, $y{int})")
    ]
)


p = figure(x_range=fruits, height=350, title="Fruit Counts",
           toolbar_location=None, tools=[hover, "pan, wheel_zoom, save"], active_scroll="wheel_zoom", sizing_mode="scale_both")

p.vbar(x=fruits, top=counts, width=0.9,border_radius=19,
             hatch_extra={ 'mycustom': ImageURLTexture(url='https://www.publicdomainpictures.net/pictures/240000/nahled/color-gradient-background.jpg') },
       hatch_pattern = dict(value="mycustom"),
      hover_fill_alpha=1,
             hover_fill_color="fill_colors", hover_line_color="black", hover_line_width=6)

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)
