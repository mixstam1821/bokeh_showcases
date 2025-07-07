# https://discourse.bokeh.org/t/expansion-of-forest-custom-animated-plot/12502
from bokeh.plotting import figure, output_file, save, curdoc, show
from bokeh.models import ColumnDataSource, Label, CustomJS
import numpy as np

treeDataURI = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAA2CAYAAADUOvnEAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA5tJREFUeNrcWE1oE0EUnp0kbWyUpCiNYEpCFSpIMdpLRTD15s2ePHixnj00N4/GoyfTg2fbiwdvvagHC1UQ66GQUIQKKgn1UAqSSFua38b3prPJZDs7s5ufKn0w7CaZ2W/fe9/73kyMRqNB3Nrj1zdn4RJ6du9T2u1a2iHYSxjP4d41oOHGQwAIwSUHIyh8/RA8XeiXh0kLGFoaXiTecw/hoTG4ZCSAaFkY0+BpsZceLtiAoV2FkepZSDk5EpppczBvpuuQCqx0YnkYcVVoqQYMyeCG+lFdaGkXeVOFNu4aEBalOBk6sbQrQF7gSdK5JXjuHXuYVIVyr0TZ0FjKDeCs6km7JYMUdrWAUVmZUBtmRnVPK+x6nIR2xomH06R35ggwJPeofWphr/W5UjPIxq8B2bKgE8C4HVHWvg+2gZjXj19PkdFztY7bk9TDCH/g6oafDPpaoMvZIRI5WyMB/0Hv++HkpTKE0kM+A+h20cPAfN4GuRyp9G+LMTW+z8rCLI8b46XO9zRcYZTde/j0AZm8WGb3Y2F9KLlE2nqYkjFLJAsDOl/lea0q55mqxXcL7YBc++bsCPMe8mUyU2ZIpnCoblca6TZA/ga2Co8PGg7UGUlEDd0ueptglbrRZLLE7poti6pCaWUo2pu1oaYI1CF9b9cCZPO3F8ikJQ/rPpQT5YETht26ss+uCIL2Y8vHwJGpA96GI5mjOlaKhowUy6BcNcgIhDviTGWCGFaqEuufWz4pgcbCh+w0gEOyOjTlTtYYlIWPYWKEsLDzOs+nhzaO1KEpd+MXpOoTUgKiNyhdy5aSMPNVqxtSsJFgza5EWA4zKtCJ2OGbLn0JSLu8+SL4G86p1Fpr7ABXdGFF/UTD4rfmFYFw4G9VAJ9SM3aF8l3yok4/J6IV9sDVb36ynmtJ2M5+CwxTYBdKNMBaocKGV2nYgkz6r+cHBP30MzAfi4Sy+BebSoPIOi8PW1PpCCvr/KOD4k9Zu0WSH0Y0+SxJ2awp/nlwKtcGyHOJ8vNHtRJzhPlsHr8MogtlVtwUU0tSM1x58upSKbfJnSKUR07GVMKkDNfXpzpv0RTHy3nZMVx5IOWdZIaPabGFvfpwpjnvfmJHXLaEvZUTseu/TeLc+xgAPhEAb/PbjO6PBaOTf6LQRh/dERde23zxLtOXbaKNhfq2L/1fAOPHDUhOpIf5485h7l+GNHHiSYPKE3Myz9sFxoJuAyazvwIMAItferha5LTqAAAAAElFTkSuQmCC'

# Parameters
begin_year, end_year = 2016, 2050
line_count = 10
columns = 18
rows = line_count

# Make tree positions
xcenters, ycenters = [], []
for row in range(rows):
    for col in range(columns):
        xcenters.append(col)
        ycenters.append(rows - row - 1)

N_trees = columns * rows

# Random permutation for "growing" order
perm = np.random.permutation(N_trees)
perm_js = ','.join(str(i) for i in perm)

source = ColumnDataSource(data=dict(
    url=[treeDataURI] * N_trees,
    x=xcenters,
    y=ycenters,
    alpha=[0.0] * N_trees,
))

plot = figure(
    width=columns*40, height=rows*60+60,
    x_range=(-0.5, columns-0.5), y_range=(-1, rows+1),
    toolbar_location=None
)
plot.axis.visible = False
plot.grid.visible = False
plot.outline_line_color = None

plot.image_url(
    url='url', x='x', y='y', w=0.9, h=0.9, anchor="center", alpha='alpha', source=source
)

year_label = Label(
    x=columns/2, y=rows+0.2,
    text=str(begin_year),
    text_align="center", text_baseline="bottom",
    text_color="green", text_font_size="38pt", text_font="Arial", name="yearlabel"
)
plot.add_layout(year_label)

callback = CustomJS(
    args=dict(
        source=source, year_label=year_label,
    ),
    code=f"""
    var begin_year = {begin_year}, end_year = {end_year};
    var total_trees = {N_trees};
    var perm = [{perm_js}];
    var current_year = begin_year;

    function set_year(year) {{
        year_label.text = year.toString();
        var fraction = (year - begin_year) / (end_year - begin_year);
        var shown = Math.round(2 + fraction * (total_trees - 2));  // starts with 2
        for (let i = 0; i < total_trees; ++i) {{
            source.data.alpha[i] = 0.0;
        }}
        for (let i = 0; i < shown; ++i) {{
            let idx = perm[i];
            source.data.alpha[idx] = 1.0;
        }}
        source.change.emit();
    }}
    set_year(current_year);

    setInterval(function() {{
        current_year++;
        if (current_year > end_year) current_year = begin_year;
        set_year(current_year);
    }}, 800);
    """
)

doc = curdoc()
doc.add_root(plot)
doc.js_on_event('document_ready', callback)

show(plot)
output_file("bokeh_trees_animate.html")
save(plot)
