# my post: https://discourse.bokeh.org/t/world-population-by-country/12530

from bokeh.plotting import figure, show, curdoc
from bokeh.models import GeoJSONDataSource, ColorBar, HoverTool, LinearColorMapper, FixedTicker
import json
import requests
from bokeh.palettes import RdYlBu as palette

# --- 1. Load world countries GeoJSON ---
url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
world_geo = requests.get(url).json()

# --- 2. Your population data ---
pop_data = [{"name": "Aruba", "value": 106445.0}, {"name": "Africa Eastern and Southern", "value": 720859132.0}, {"name": "Afghanistan", "value": 41128771.0}, {"name": "Africa Western and Central", "value": 490330870.0}, {"name": "Angola", "value": 35588987.0}, {"name": "Albania", "value": 2777689.0}, {"name": "Andorra", "value": 79824.0}, {"name": "Arab World", "value": 464684914.0}, {"name": "United Arab Emirates", "value": 9441129.0}, {"name": "Argentina", "value": 46234830.0}, {"name": "Armenia", "value": 2780469.0}, {"name": "American Samoa", "value": 44273.0}, {"name": "Antigua and Barbuda", "value": 93763.0}, {"name": "Australia", "value": 26005540.0}, {"name": "Austria", "value": 9041851.0}, {"name": "Azerbaijan", "value": 10141756.0}, {"name": "Burundi", "value": 12889576.0}, {"name": "Belgium", "value": 11685814.0}, {"name": "Benin", "value": 13352864.0}, {"name": "Burkina Faso", "value": 22673762.0}, {"name": "Bangladesh", "value": 171186372.0}, {"name": "Bulgaria", "value": 6465097.0}, {"name": "Bahrain", "value": 1472233.0}, {"name": "Bahamas, The", "value": 409984.0}, {"name": "Bosnia and Herzegovina", "value": 3233526.0}, {"name": "Belarus", "value": 9228071.0}, {"name": "Belize", "value": 405272.0}, {"name": "Bermuda", "value": 63532.0}, {"name": "Bolivia", "value": 12224110.0}, {"name": "Brazil", "value": 215313498.0}, {"name": "Barbados", "value": 281635.0}, {"name": "Brunei Darussalam", "value": 449002.0}, {"name": "Bhutan", "value": 782455.0}, {"name": "Botswana", "value": 2630296.0}, {"name": "Central African Republic", "value": 5579144.0}, {"name": "Canada", "value": 38929902.0}, {"name": "Central Europe and the Baltics", "value": 100108221.0}, {"name": "Switzerland", "value": 8775760.0}, {"name": "Channel Islands", "value": 174079.0}, {"name": "Chile", "value": 19603733.0}, {"name": "China", "value": 1412175000.0}, {"name": "Ivory Coast", "value": 28160542.0}, {"name": "Cameroon", "value": 27914536.0}, {"name": "Dem. Rep. Congo", "value": 99010212.0}, {"name": "Congo", "value": 5970424.0}, {"name": "Colombia", "value": 51874024.0}, {"name": "Comoros", "value": 836774.0}, {"name": "Cabo Verde", "value": 593149.0}, {"name": "Costa Rica", "value": 5180829.0}, {"name": "Caribbean small states", "value": 7505478.0}, {"name": "Cuba", "value": 11212191.0}, {"name": "Curacao", "value": 149996.0}, {"name": "Cayman Islands", "value": 68706.0}, {"name": "Cyprus", "value": 1251488.0}, {"name": "Czech Rep.", "value": 10672118.0}, {"name": "Germany", "value": 83797985.0}, {"name": "Djibouti", "value": 1120849.0}, {"name": "Dominica", "value": 72737.0}, {"name": "Denmark", "value": 5903037.0}, {"name": "Dominican Rep.", "value": 11228821.0}, {"name": "Algeria", "value": 44903225.0}, {"name": "East Asia & Pacific (excluding high income)", "value": 2129112126.0}, {"name": "Early-demographic dividend", "value": 3447398652.0}, {"name": "East Asia & Pacific", "value": 2375162207.0}, {"name": "Europe & Central Asia (excluding high income)", "value": 397824705.0}, {"name": "Europe & Central Asia", "value": 920375568.0}, {"name": "Ecuador", "value": 18001000.0}, {"name": "Egypt", "value": 110990103.0}, {"name": "Euro area", "value": 344475911.0}, {"name": "Eritrea", "value": 3684032.0}, {"name": "Spain", "value": 47778340.0}, {"name": "Estonia", "value": 1348840.0}, {"name": "Ethiopia", "value": 123379924.0}, {"name": "European Union", "value": 447370510.0}, {"name": "Fragile and conflict affected situations", "value": 1019139254.0}, {"name": "Finland", "value": 5556106.0}, {"name": "Fiji", "value": 929766.0}, {"name": "France", "value": 67971311.0}, {"name": "Faroe Islands", "value": 53090.0}, {"name": "Micronesia, Fed. Sts.", "value": 114164.0}, {"name": "Gabon", "value": 2388992.0}, {"name": "United Kingdom", "value": 66971395.0}, {"name": "Georgia", "value": 3712502.0}, {"name": "Ghana", "value": 33475870.0}, {"name": "Gibraltar", "value": 32649.0}, {"name": "Guinea", "value": 13859341.0}, {"name": "Gambia", "value": 2705992.0}, {"name": "Guinea Bissau", "value": 2105566.0}, {"name": "Equatorial Guinea", "value": 1674908.0}, {"name": "Greece", "value": 10426919.0}, {"name": "Grenada", "value": 125438.0}, {"name": "Greenland", "value": 56661.0}, {"name": "Guatemala", "value": 17357886.0}, {"name": "Guam", "value": 171774.0}, {"name": "Guyana", "value": 808726.0}, {"name": "High income", "value": 1244364814.0}, {"name": "Hong Kong SAR, China", "value": 7346100.0}, {"name": "Honduras", "value": 10432860.0}, {"name": "Heavily indebted poor countries (HIPC)", "value": 884288332.0}, {"name": "Croatia", "value": 3855600.0}, {"name": "Haiti", "value": 11584996.0}, {"name": "Hungary", "value": 9643048.0}, {"name": "IBRD only", "value": 4913887020.0}, {"name": "IDA & IBRD total", "value": 6754029970.0}, {"name": "IDA total", "value": 1840142950.0}, {"name": "IDA blend", "value": 607735968.0}, {"name": "Indonesia", "value": 275501339.0}, {"name": "IDA only", "value": 1232406982.0}, {"name": "Isle of Man", "value": 84519.0}, {"name": "India", "value": 1417173173.0}, {"name": "Ireland", "value": 5127170.0}, {"name": "Iran", "value": 88550570.0}, {"name": "Iraq", "value": 44496122.0}, {"name": "Iceland", "value": 382003.0}, {"name": "Israel", "value": 9557500.0}, {"name": "Italy", "value": 58940425.0}, {"name": "Jamaica", "value": 2827377.0}, {"name": "Jordan", "value": 11285869.0}, {"name": "Japan", "value": 125124989.0}, {"name": "Kazakhstan", "value": 19621972.0}, {"name": "Kenya", "value": 54027487.0}, {"name": "Kyrgyzstan", "value": 6974900.0}, {"name": "Cambodia", "value": 16767842.0}, {"name": "Kiribati", "value": 131232.0}, {"name": "St. Kitts and Nevis", "value": 47657.0}, {"name": "Korea", "value": 51628117.0}, {"name": "Kuwait", "value": 4268873.0}, {"name": "Latin America & Caribbean (excluding high income)", "value": 596596955.0}, {"name": "Laos", "value": 7529475.0}, {"name": "Lebanon", "value": 5489739.0}, {"name": "Liberia", "value": 5302681.0}, {"name": "Libya", "value": 6812341.0}, {"name": "St. Lucia", "value": 179857.0}, {"name": "Latin America & Caribbean", "value": 659310564.0}, {"name": "Least developed countries: UN classification", "value": 1125179454.0}, {"name": "Low income", "value": 703727949.0}, {"name": "Liechtenstein", "value": 39327.0}, {"name": "Sri Lanka", "value": 22181000.0}, {"name": "Lower middle income", "value": 3190184199.0}, {"name": "Low & middle income", "value": 6678280291.0}, {"name": "Lesotho", "value": 2305825.0}, {"name": "Late-demographic dividend", "value": 2325542891.0}, {"name": "Lithuania", "value": 2831639.0}, {"name": "Luxembourg", "value": 653103.0}, {"name": "Latvia", "value": 1879383.0}, {"name": "Macao SAR, China", "value": 695168.0}, {"name": "St. Martin (French part)", "value": 31791.0}, {"name": "Morocco", "value": 37457971.0}, {"name": "Monaco", "value": 36469.0}, {"name": "Moldova", "value": 2538894.0}, {"name": "Madagascar", "value": 29611714.0}, {"name": "Maldives", "value": 523787.0}, {"name": "Middle East & North Africa", "value": 493279469.0}, {"name": "Mexico", "value": 127504125.0}, {"name": "Marshall Islands", "value": 41569.0}, {"name": "Middle income", "value": 5974552342.0}, {"name": "Macedonia", "value": 2057679.0}, {"name": "Mali", "value": 22593590.0}, {"name": "Malta", "value": 531113.0}, {"name": "Myanmar", "value": 54179306.0}, {"name": "Middle East & North Africa (excluding high income)", "value": 424328381.0}, {"name": "Montenegro", "value": 617213.0}, {"name": "Mongolia", "value": 3398366.0}, {"name": "Northern Mariana Islands", "value": 49551.0}, {"name": "Mozambique", "value": 32969518.0}, {"name": "Mauritania", "value": 4736139.0}, {"name": "Mauritius", "value": 1262523.0}, {"name": "Malawi", "value": 20405317.0}, {"name": "Malaysia", "value": 33938221.0}, {"name": "North America", "value": 372280991.0}, {"name": "Namibia", "value": 2567012.0}, {"name": "New Caledonia", "value": 269220.0}, {"name": "Niger", "value": 26207977.0}, {"name": "Nigeria", "value": 218541212.0}, {"name": "Nicaragua", "value": 6948392.0}, {"name": "Netherlands", "value": 17700982.0}, {"name": "Norway", "value": 5457127.0}, {"name": "Nepal", "value": 30547580.0}, {"name": "Nauru", "value": 12668.0}, {"name": "New Zealand", "value": 5124100.0}, {"name": "OECD members", "value": 1376606817.0}, {"name": "Oman", "value": 4576298.0}, {"name": "Other small states", "value": 33169026.0}, {"name": "Pakistan", "value": 235824862.0}, {"name": "Panama", "value": 4408581.0}, {"name": "Peru", "value": 34049588.0}, {"name": "Philippines", "value": 115559009.0}, {"name": "Palau", "value": 18055.0}, {"name": "Papua New Guinea", "value": 10142619.0}, {"name": "Poland", "value": 36821749.0}, {"name": "Pre-demographic dividend", "value": 1038012552.0}, {"name": "Puerto Rico", "value": 3221789.0}, {"name": "Dem. Rep. Korea", "value": 26069416.0}, {"name": "Portugal", "value": 10409704.0}, {"name": "Paraguay", "value": 6780744.0}, {"name": "West Bank and Gaza", "value": 5043612.0}, {"name": "Pacific island small states", "value": 2639019.0}, {"name": "Post-demographic dividend", "value": 1113495082.0}, {"name": "French Polynesia", "value": 306279.0}, {"name": "Qatar", "value": 2695122.0}, {"name": "Romania", "value": 19047009.0}, {"name": "Russia", "value": 144236933.0}, {"name": "Rwanda", "value": 13776698.0}, {"name": "South Asia", "value": 1919348000.0}, {"name": "Saudi Arabia", "value": 36408820.0}, {"name": "Sudan", "value": 46874204.0}, {"name": "Senegal", "value": 17316449.0}, {"name": "Singapore", "value": 5637022.0}, {"name": "Solomon Islands", "value": 724273.0}, {"name": "Sierra Leone", "value": 8605718.0}, {"name": "El Salvador", "value": 6336392.0}, {"name": "San Marino", "value": 33660.0}, {"name": "Somalia", "value": 17597511.0}, {"name": "Republic of Serbia", "value": 6664449.0}, {"name": "Sub-Saharan Africa (excluding high income)", "value": 1211070124.0}, {"name": "South Sudan", "value": 10913164.0}, {"name": "Sub-Saharan Africa", "value": 1211190002.0}, {"name": "Small states", "value": 43313523.0}, {"name": "Sao Tome and Principe", "value": 227380.0}, {"name": "Suriname", "value": 618040.0}, {"name": "Slovakia", "value": 5431752.0}, {"name": "Slovenia", "value": 2111986.0}, {"name": "Sweden", "value": 10486941.0}, {"name": "Eswatini", "value": 1201670.0}, {"name": "Sint Maarten (Dutch part)", "value": 42848.0}, {"name": "Seychelles", "value": 119878.0}, {"name": "Syria", "value": 22125249.0}, {"name": "Turks and Caicos Islands", "value": 45703.0}, {"name": "Chad", "value": 17723315.0}, {"name": "East Asia & Pacific (IDA & IBRD countries)", "value": 2103055378.0}, {"name": "Europe & Central Asia (IDA & IBRD countries)", "value": 457549063.0}, {"name": "Togo", "value": 8848699.0}, {"name": "Thailand", "value": 71697030.0}, {"name": "Tajikistan", "value": 9952787.0}, {"name": "Turkmenistan", "value": 6430770.0}, {"name": "Latin America & the Caribbean (IDA & IBRD countries)", "value": 643602758.0}, {"name": "Timor-Leste", "value": 1341296.0}, {"name": "Middle East & North Africa (IDA & IBRD countries)", "value": 419284769.0}, {"name": "Tonga", "value": 106858.0}, {"name": "South Asia (IDA & IBRD)", "value": 1919348000.0}, {"name": "Sub-Saharan Africa (IDA & IBRD countries)", "value": 1211190002.0}, {"name": "Trinidad and Tobago", "value": 1531044.0}, {"name": "Tunisia", "value": 12356117.0}, {"name": "Turkey", "value": 84979913.0}, {"name": "Tuvalu", "value": 11312.0}, {"name": "United Republic of Tanzania", "value": 65497748.0}, {"name": "Uganda", "value": 47249585.0}, {"name": "Ukraine", "value": 38000000.0}, {"name": "Upper middle income", "value": 2784368143.0}, {"name": "Uruguay", "value": 3422794.0}, {"name": "United States", "value": 333287557.0}, {"name": "Uzbekistan", "value": 35648100.0}, {"name": "St. Vincent and the Grenadines", "value": 103948.0}, {"name": "Venezuela", "value": 28301696.0}, {"name": "British Virgin Islands", "value": 31305.0}, {"name": "Virgin Islands (U.S.)", "value": 105413.0}, {"name": "Vietnam", "value": 98186856.0}, {"name": "Vanuatu", "value": 326740.0}, {"name": "World", "value": 7950946801.0}, {"name": "Samoa", "value": 222382.0}, {"name": "Kosovo", "value": 1761985.0}, {"name": "Yemen", "value": 33696614.0}, {"name": "South Africa", "value": 59893885.0}, {"name": "Zambia", "value": 20017675.0}, {"name": "Zimbabwe", "value": 16320537.0}]

# --- 3. Convert to dictionary for fast lookup ---
pop_dict = {item['name']: item['value'] for item in pop_data}

# --- 4. Assign population data to each country in GeoJSON ---
for feature in world_geo['features']:
    country = feature['properties']['name']
    value = pop_dict.get(country, None)
    # Country name fallbacks
    if value is None:
        if country == 'United States of America': value = pop_dict.get('United States')
        elif country == 'Russian Federation': value = pop_dict.get('Russia')
        elif country == 'Czech Republic': value = pop_dict.get('Czech Rep.')
        elif country == "Democratic Republic of the Congo": value = pop_dict.get("Dem. Rep. Congo")
        elif country == "Republic of the Congo": value = pop_dict.get("Congo")
        elif country == "Korea, Republic of": value = pop_dict.get("Korea")
        elif country == "Egypt, Arab Rep.": value = pop_dict.get("Egypt")
        # ... add more custom matches if needed
    feature['properties']['population'] = value

# (Optional) Remove countries with no data
world_geo['features'] = [f for f in world_geo['features'] if f['properties']['population'] is not None]

# --- 5. BINNING: Discrete Population Bins & Labels (logarithmic) ---
bin_edges = [0, 5e5, 2e6, 1e7,3e7, 5e7, 1e8, 3e8, 1e9, 2e9]
bin_labels = [
    "<500k", "500k–2M", "2M–10M", "10M–30M","30M–50M",
    "50M–100M", "100M–300M", "300M–1B", "1B+"
]
# palette = [
#     '#e31a1c',  # Red (smallest)
#     '#fd8d3c',  # Orange
#     '#fecc5c',  # Yellow
#     '#ffffb2',  # Light yellow
#     '#a1d99b',  # Light green
#     '#31a354',  # Green
#     '#3182bd',  # Blue
#     '#756bb1',  # Purple
#     '#636363',  # Dark grey (largest)
# ][::-1]


for feature in world_geo['features']:
    pop = feature['properties']['population']
    # Assign a bin index
    idx = next((i for i in range(len(bin_edges)-1) if bin_edges[i] <= pop < bin_edges[i+1]), len(bin_labels)-1)
    feature['properties']['pop_bin_index'] = idx

# --- 6. Bokeh data source ---
geosource = GeoJSONDataSource(geojson=json.dumps(world_geo))

# --- 7. Discrete Palette & ColorMapper ---
# palette = list(Set3[len(bin_labels)])  # 9 colors
color_mapper = LinearColorMapper(palette=palette[9], low=0, high=len(bin_labels)-1)

# --- 8. Build Bokeh plot ---
p = figure(
    title="🌎 World Population by Country for 2022: from The World Bank (SP.POP.TOTL)",
    width=1200, height=650,
    toolbar_location='right',
    tools='pan,box_zoom,reset,save,wheel_zoom', active_scroll = 'wheel_zoom',
    x_axis_location=None, y_axis_location=None
)
p.grid.grid_line_color = None
p.axis.visible = False


countries = p.patches(
    'xs', 'ys',
    source=geosource,
    fill_color={'field': 'pop_bin_index', 'transform': color_mapper},
    line_color='black',
    line_width=0.25,
    fill_alpha=0.8,
                         hover_line_color='black',hover_line_width=5,

)

# --- 9. Hover tool ---
hover = HoverTool(renderers=[countries],attachment="above",show_arrow=False, tooltips=
                  """<div style="background-color: #f0f0f0; padding: 5px; margin-bottom:30px; border-radius: 5px; box-shadow: 0px 0px 5px rgba(0,0,0,0.3);">        <font size="5" style="background-color: #f0f0f0; padding: 5px; border-radius: 5px;">
            <i>Country:</i> <b>@name</b> <br> 
            <i>Population:</i> <b>@population{0,0}</b> <br>
        </font> </div> <style> :host { --tooltip-border: transparent;  /* Same border color used everywhere */ --tooltip-color: transparent; --tooltip-text: #2f2f2f;} </style> """
                )
p.add_tools(hover)

# --- 10. Discrete ColorBar ---
color_bar = ColorBar(
    color_mapper=color_mapper,
    ticker=FixedTicker(ticks=list(range(len(bin_labels)))),
    major_label_overrides={i: l for i, l in enumerate(bin_labels)},
    label_standoff=12,
    width=24,
    height=600,
    border_line_color=None,
    background_fill_color='#f5f5f5',
    location=(0,10),
    orientation='vertical',
    title='Population',
    major_label_text_color="#2f2f2f", 
    title_text_color="#2f2f2f", 


)
p.add_layout(color_bar, 'right')

# --- 11. Style ---
p.title.text_font_size = '19pt'
p.title.text_font = 'Montserrat'
p.title.text_color = '#7b4397'
p.background_fill_color = '#f5f5f5'
p.border_fill_color = '#f5f5f5'

show(p)
