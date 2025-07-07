https://discourse.bokeh.org/t/custom-design-for-widgets/12479/4
from bokeh.io import curdoc
from bokeh.models import TableColumn, ColumnDataSource, DataTable, InlineStyleSheet
from bokeh.layouts import column
import numpy as np
import pandas as pd

# --- Example DataFrame ---
np.random.seed(0)
n = 30
df = pd.DataFrame({
    "Year": np.arange(2000, 2000 + n),
    "Value": np.round(np.random.normal(10, 2, n), 2),
    "Anomaly": np.round(np.random.normal(0, 1, n), 2)
})

# --- Bokeh DataTable setup ---
source5 = ColumnDataSource(df)

columns5 = [
    TableColumn(field="Year", title="Year"),
    TableColumn(field="Value", title="Value"),
    TableColumn(field="Anomaly", title="Anomaly")
]

# --- Your custom dark theme stylesheet ---
dark_table_style = InlineStyleSheet(css="""
/* Container styling */
:host {
    background: #2e2e30 !important;
    border-radius: 14px !important;
    padding: 16px !important;
    box-shadow: 0 4px 18px #0006 !important;
    margin: 10px !important;
}

/* Headers */
:host div[class*="header"],
:host div[class*="slick-header"],
:host th,
:host [class*="header"] {
    background: #2e2e30 !important;
    color: #34ffe0 !important;
    font-weight: bold !important;
    font-family: 'Fira Code', monospace !important;
    border-bottom: 1px solid #06b6d4 !important;
}

/* cells */
:host div[class*="cell"],
:host div[class*="slick-cell"],
:host td {
    background: #565755 !important;
    color: #ef5f5f !important;
    border-right: 1px solid #908e8e !important;
    border-bottom: 1px solid #908e8e !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 1.2em !important;

}

/* Alternating rows */
:host div[class*="row"]:nth-child(even) div[class*="cell"],
:host div[class*="slick-row"]:nth-child(even) div[class*="slick-cell"],
:host tr:nth-child(even) td {
    background: #2a2a2c !important;
    color: #ffb907 !important;
    border-right: 1px solid #908e8e !important;
    border-bottom: 1px solid #908e8e !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 0.9em !important;
}

/* Hover effects */
:host div[class*="row"]:hover div[class*="cell"],
:host div[class*="slick-row"]:hover div[class*="slick-cell"],
:host tr:hover td {
    background: #3eafff !important;
    color: #0c0c0c !important;
    border-color: #ff0000 !important;
    border-style: solid !important;
    border-width: 1px !important;
}

/* Selected cells */
:host div[class*="slick-cell"][class*="selected"],
:host div[class*="cell"][class*="selected"] {
    background: pink !important;
    color: red !important;
    border: 1px solid #ff1493 !important;
}
                                    
/* Selected cells */
:host div[class*="row"]:nth-child(even) div[class*="cell"][class*="selected"],
:host div[class*="slick-row"]:nth-child(even) div[class*="slick-cell"][class*="selected"]{
    background: pink !important;
    color: black !important;
    border: 1px solid #ff1493 !important;
}

/* Scrollbars */
:host *::-webkit-scrollbar {
    width: 9px !important;
    height: 8px !important;
    background: #1a1a2e !important;
}
:host *::-webkit-scrollbar-thumb {
    background: #06b6d4 !important;
    border-radius: 4px !important;
}
:host *::-webkit-scrollbar-track {
    background: #1c2e1a !important;
    border-radius: 4px !important;
}
/* Firefox scrollbars */
:host .bk-data-table {
    scrollbar-color: #06b6d4 #1c2e1a !important;
    scrollbar-width: thin !important;
}

/* But restore specific dark backgrounds where needed */
:host div[class*="header"] * {
    background-color: #1a1a2e !important;
}

:host [class*="header"] * {
    color: #34ffe0 !important;
}
""")

# --- DataTable Widget ---
data_table = DataTable(
    source=source5,
    columns=columns5,
    width=500,
    height=450,
    row_height=21,
    stylesheets=[dark_table_style],
    selectable=True,
    sortable=True,
    editable=True,     # Enable cell editing

)

# --- Show in Bokeh document ---
curdoc().add_root(column(data_table))
