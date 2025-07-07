https://discourse.bokeh.org/t/update-plot-with-editable-table-in-toolbar/12500

import numpy as np
from bokeh.plotting import figure, save, output_file
from bokeh.models import (
    ColumnDataSource, HoverTool, CustomAction, CustomJS,
    DataTable, TableColumn, NumberEditor, StringEditor, TextInput, Button
)
from bokeh.layouts import column, row

# ---- Generate random data for bar plot ----
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
values = [151,168,193,223,240,245,238,221,195,170,154,150]

bar_data_source = ColumnDataSource(dict(x=months, y=values))

# ---- Bar plot ----
bar_plot = figure(
    width=800, height=500, title='Interactive Bar Plot with Editable Data',
    x_range=bar_data_source.data["x"]
)
bar_plot.xaxis.axis_label = 'Categories'
bar_plot.yaxis.axis_label = 'Values'
bars = bar_plot.vbar(
    x='x', top='y', width=0.8, source=bar_data_source,
    fill_color='steelblue', line_color='black', alpha=0.8,
    hover_fill_color='navy', hover_line_color='white'
)

bar_plot.add_tools(HoverTool(tooltips=[('Category', '@x'), ('Value', '@y')], renderers=[bars]))

# ---- Data Table ----
columns = [
    TableColumn(field="x", title="Category (X)", editor=StringEditor()),   # Accepts text!
    TableColumn(field="y", title="Value (Y)", editor=NumberEditor())
]
data_table = DataTable(source=bar_data_source, columns=columns, width=400, height=300, editable=True)

# Input fields for adding new data
new_x_input = TextInput(value="", title="New Category:", width=120)
new_y_input = TextInput(value="", title="New Value:", width=120)
add_button = Button(label="Add Data Point", button_type="success", width=120)

# Initially hide the table and inputs
data_table.visible = False
new_x_input.visible = False
new_y_input.visible = False
add_button.visible = False

# ---- Custom toolbar action for data table ----
table_callback = CustomJS(
    args=dict(
        data_table=data_table,
        new_x_input=new_x_input,
        new_y_input=new_y_input,
        add_button=add_button,
    ),
    code="""
    const currently_visible = data_table.visible;
    data_table.visible = !currently_visible;
    new_x_input.visible = !currently_visible;
    new_y_input.visible = !currently_visible;
    add_button.visible = !currently_visible;
    """
)

table_action = CustomAction(
    icon="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cGF0aCBkPSJNMyAzaDE4djE4SDNWMyIgc3Ryb2tlPSIjMDA3YWNjIiBzdHJva2Utd2lkdGg9IjIiIGZpbGw9Im5vbmUiLz4KICA8cGF0aCBkPSJNMyA5aDE4IiBzdHJva2U9IiMwMDdhY2MiIHN0cm9rZS13aWR0aD0iMiIvPgogIDxwYXRoIGQ9Ik0zIDE1aDE4IiBzdHJva2U9IiMwMDdhY2MiIHN0cm9rZS13aWR0aD0iMiIvPgogIDxwYXRoIGQ9Ik05IDNoMTIiIHN0cm9rZT0iIzAwN2FjYyIgc3Ryb2tlLXdpZHRoPSIyIi8+CiAgPHBhdGggZD0iTTE1IDNoNiIgc3Ryb2tlPSIjMDA3YWNjIiBzdHJva2Utd2lkdGg9IjIiLz4KPC9zdmc+",
    description="Toggle Data Table",
    callback=table_callback
)
bar_plot.add_tools(table_action)

# ---- CustomJS callback for updating bar plot when data changes ----
update_bar_callback = CustomJS(
    args=dict(
        source=bar_data_source,
        plot=bar_plot
    ),
    code="""
    // Update bar plot x_range to accommodate new data
    const new_x_values = source.data['x'].map(x => x.toString());
    plot.x_range.factors = new_x_values;
    """
)

# ---- CustomJS callback for adding new data point ----
add_data_callback = CustomJS(
    args=dict(
        source=bar_data_source,
        x_input=new_x_input,
        y_input=new_y_input,
        plot=bar_plot
    ),
    code="""
    try {
        const new_x = x_input.value;  // Accept as string!
        const new_y = parseFloat(y_input.value);

        if (!new_x || isNaN(new_y)) {
            return;
        }

        // Get current data as arrays
        const current_x = Array.from(source.data['x']);
        const current_y = Array.from(source.data['y']);

        // Add new point
        current_x.push(new_x);
        current_y.push(new_y);

        // Update data source
        source.data = {
            'x': current_x,
            'y': current_y
        };

        // Update bar plot x_range
        const new_x_values = current_x.map(x => x.toString());
        plot.x_range.factors = new_x_values;

        // Clear input fields
        x_input.value = "";
        y_input.value = "";

    } catch (error) {
        console.log("Error adding data point:", error);
    }
    """
)

# Attach callbacks
bar_data_source.js_on_change('data', update_bar_callback)
add_button.js_on_click(add_data_callback)

# ---- Layout ----
input_row = row(new_x_input, new_y_input, add_button)
table_section = column(data_table, input_row)

layout = row(
    bar_plot,
    table_section
)

# Save to HTML file
output_file("interactive_bar_plot_with_table.html")
save(layout)
