# check out my post here: https://discourse.bokeh.org/t/heatmap-calendar/12237

from bokeh.plotting import curdoc, figure, show
from bokeh.models import (ColumnDataSource, ColorBar, LinearColorMapper, HoverTool,
                         BoxAnnotation, Label, Range1d, Title, Span)
from bokeh.layouts import column, row
from bokeh.palettes import YlOrRd as palette
# from bokeh.palettes import Greens as palette
# from bokeh.palettes import Cividis as palette

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import calendar


curdoc().theme = 'dark_minimal'
# Generate data for 2024 (leap year - 366 days)
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=x) for x in range(366)]

# Create more sophisticated random activity data
np.random.seed(42)
base = np.random.normal(50, 20, size=366)
weekday_boost = np.array([1.4 if d.weekday() < 5 else 0.6 for d in dates])
seasonal_pattern = np.sin(np.linspace(0, 2*np.pi, 366)) * 15 + 5
monthly_pattern = np.sin(np.linspace(0, 24*np.pi, 366)) * 10
trend = np.linspace(0, 20, 366)

values = (base * weekday_boost + seasonal_pattern + monthly_pattern + trend)
values = np.clip(values, 0, 100).astype(int)

# Create DataFrame with proper week calculation
data = {
    'date': dates,
    'value': values,
    'weekday': [d.weekday() for d in dates],
    'month': [d.month for d in dates],
    'day': [d.day for d in dates],
    'date_str': [d.strftime('%Y-%m-%d') for d in dates],
    'day_name': [d.strftime('%A') for d in dates],
    'month_name': [d.strftime('%B') for d in dates],
    'week_of_month': [int((d.day - 1) / 7) + 1 for d in dates]
}
df = pd.DataFrame(data)

# Calculate the week number relative to the start of the year
current_week = 0
prev_month = 1
week_numbers = []

for _, row in df.iterrows():
    if row['month'] != prev_month:
        if row['weekday'] != 0:  # If month doesn't start on Monday
            current_week += 1
        prev_month = row['month']
    if row['weekday'] == 0:  # Start new week on Monday
        current_week += 1
    week_numbers.append(current_week)

df['week'] = week_numbers

# Calculate statistics
daily_avg = df['value'].mean()
weekday_avgs = df.groupby('weekday')['value'].mean()
month_avgs = df.groupby('month')['value'].mean()
max_day = df.loc[df['value'].idxmax()]
min_day = df.loc[df['value'].idxmin()]

# Create ColumnDataSource
source = ColumnDataSource(df)

# Create color mapper
colors = palette[6][::-1]
mapper = LinearColorMapper(palette=colors, low=0, high=100)

# Create main figure
p = figure(title='Activity Calendar 2024',
           width=1200, height=300,
           x_range=(0.5, 64), y_range=(-0.5, 6.5),
           tools="hover,save,pan,box_zoom,reset",
           toolbar_location='above',
#               background_fill_color="#1e1e1e",  # Dark background
#     border_fill_color="#1e1e1e"  # Dark border
          )

# Add rectangles for each day
rect = p.rect(x='week', y='weekday',
              width=0.9, height=0.9,
              source=source,
              fill_color={'field': 'value', 'transform': mapper},
              line_color='white',
              line_alpha=0.9,
             hover_line_color="lime",
                          hover_line_width=3,line_cap='round'

             )

# Enhanced hover tool
hover = p.select_one(HoverTool)
hover.tooltips = """<div style="background-color: #f0f0f0; padding: 5px; border-radius: 5px; box-shadow: 0px 0px 5px rgba(0,0,0,0.3);">        <font size="5" style="background-color: #f0f0f0; padding: 5px; border-radius: 5px;">
            <i>Date:</i> <b>@date_str</b> <br> 
            <i>Day:</i> <b>@day_name</b> <br>
            <i>Activity:</i> <b>@value%</b> <br> 
            <i>Month:</i> <b>@month_name</b> <br>
        </font> </div> <style> :host { --tooltip-border: transparent;  /* Same border color used everywhere */ --tooltip-color: transparent; --tooltip-text: #2f2f2f;} </style> """



# hover.tooltips.position = (90,90)
# hover.show_arrow = False
hover.attachment='left'
hover.anchor='left'
# hover.point_policy = 'snap_to_data'






# Customize appearance
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.minor_tick_line_color = None
p.grid.grid_line_color = None
p.outline_line_color = None

# Add weekday labels
weekday_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
p.yaxis.ticker = list(range(7))
p.yaxis.major_label_overrides = {i: day for i, day in enumerate(weekday_labels)}

# Add month labels and separators
month_weeks = {}
month_separators = []
prev_week = 0

for month in range(1, 13):
    month_data = df[df['month'] == month]
    if not month_data.empty:
        first_week = month_data['week'].min()
        last_week = month_data['week'].max()
        month_weeks[month] = (first_week + last_week) / 2
        
        # Add vertical separator between months
        if month > 1:
            separator = Span(location=first_week - 0.5, dimension='height',
                           line_color='#666666', line_width=1, line_alpha=0.3)
            p.add_layout(separator)

month_positions = list(month_weeks.values())
month_labels = [calendar.month_name[month] for month in month_weeks.keys()]

p.xaxis.ticker = month_positions
p.xaxis.major_label_overrides = {pos: label for pos, label in zip(month_positions, month_labels)}

# # Highlight weekends
# weekend_box = BoxAnnotation(fill_color='gray', fill_alpha=0.05,
#                            bottom=4.5, top=6.5)
# p.add_layout(weekend_box)

# Add color bar
color_bar = ColorBar(
    color_mapper=mapper,
    location=(0, 0),
    title='Activity Level (%)',
    orientation='horizontal',
    padding=0,
    bar_line_color=None,
    title_text_font_size='10pt',
    major_label_text_font_size='8pt'
)
p.add_layout(color_bar, 'below')

# Add statistics as subtitles
stats_text = [
    f"Yearly Average: {daily_avg:.1f}%"+"   "+ f"Most Active: {max_day['date_str']} ({max_day['value']}%)" +"   "+ f"Least Active: {min_day['date_str']} ({min_day['value']}%)"
]

for i, text in enumerate(stats_text):
    p.add_layout(Title(text=text, text_font_size='10pt', text_color='#666666'), 'below')

# Style the plot
p.title.text_font_size = '16pt'
p.title.text_font = 'helvetica'
p.title.text_color = '#2b83ba'
p.axis.axis_label = None
p.axis.major_label_text_font_size = '9pt'
# p.axis.major_label_text_color = '#666666'
p.axis.major_label_text_font_style = 'bold'

# Add explanatory text
p.add_layout(Label(
    x=-1, y=-1,
    text='Weekend',
    text_color='#666666',
    text_font_size='8pt'
))

# Show the plot
show(p)
