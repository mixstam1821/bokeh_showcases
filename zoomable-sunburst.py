# my post: https://discourse.bokeh.org/t/zoomable-sunburst/12549

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, HoverTool, TapTool, Button, Div
from bokeh.plotting import figure, curdoc
from bokeh.server.server import Server
import numpy as np
import math
from typing import Dict, List, Any
from bokeh.palettes import Category10
# Define discrete colors for parent nodes
PALETTE = Category10[10]  # 10 strong, discrete colors for top-level parents

# Sample hierarchical data - replace with your own
sample_data = {
    "name": "Company Organization",
    "children": [
        {
            "name": "Technology",
            "children": [
                {
                    "name": "Frontend Development",
                    "children": [
                        {
                            "name": "React Ecosystem",
                            "children": [
                                {"name": "React Core", "value": 25},
                                {"name": "Next.js", "value": 20},
                                {"name": "React Native", "value": 15},
                                {"name": "Redux/Zustand", "value": 12}
                            ]
                        },
                        {
                            "name": "Vue Ecosystem", 
                            "children": [
                                {"name": "Vue 3", "value": 18},
                                {"name": "Nuxt.js", "value": 12},
                                {"name": "Vuex/Pinia", "value": 8}
                            ]
                        },
                        {
                            "name": "Other Frameworks",
                            "children": [
                                {"name": "Angular", "value": 15},
                                {"name": "Svelte", "value": 8},
                                {"name": "Vanilla JS", "value": 10}
                            ]
                        }
                    ]
                },
                {
                    "name": "Backend Development", 
                    "children": [
                        {
                            "name": "Python Stack",
                            "children": [
                                {"name": "Django", "value": 22},
                                {"name": "FastAPI", "value": 18},
                                {"name": "Flask", "value": 15},
                                {"name": "Data Science", "value": 20}
                            ]
                        },
                        {
                            "name": "Node.js Stack",
                            "children": [
                                {"name": "Express.js", "value": 15},
                                {"name": "NestJS", "value": 12},
                                {"name": "Koa.js", "value": 8}
                            ]
                        },
                        {
                            "name": "Other Languages",
                            "children": [
                                {"name": "Java Spring", "value": 18},
                                {"name": "C# .NET", "value": 16},
                                {"name": "Go", "value": 12},
                                {"name": "Rust", "value": 8}
                            ]
                        }
                    ]
                },
                {
                    "name": "DevOps & Infrastructure",
                    "children": [
                        {
                            "name": "Cloud Platforms",
                            "children": [
                                {"name": "AWS", "value": 35},
                                {"name": "Google Cloud", "value": 25},
                                {"name": "Azure", "value": 20},
                                {"name": "Digital Ocean", "value": 10}
                            ]
                        },
                        {
                            "name": "Containerization",
                            "children": [
                                {"name": "Docker", "value": 30},
                                {"name": "Kubernetes", "value": 20},
                                {"name": "Podman", "value": 5}
                            ]
                        },
                        {"name": "CI/CD", "value": 25},
                        {"name": "Monitoring", "value": 15}
                    ]
                },
                {
                    "name": "Mobile Development",
                    "children": [
                        {"name": "iOS Native", "value": 25},
                        {"name": "Android Native", "value": 30},
                        {"name": "Flutter", "value": 20},
                        {"name": "React Native", "value": 18},
                        {"name": "Xamarin", "value": 7}
                    ]
                },
                {
                    "name": "Data & AI",
                    "children": [
                        {
                            "name": "Machine Learning",
                            "children": [
                                {"name": "TensorFlow", "value": 20},
                                {"name": "PyTorch", "value": 18},
                                {"name": "Scikit-learn", "value": 15},
                                {"name": "Hugging Face", "value": 12}
                            ]
                        },
                        {
                            "name": "Data Engineering",
                            "children": [
                                {"name": "Apache Spark", "value": 15},
                                {"name": "Airflow", "value": 12},
                                {"name": "Kafka", "value": 10}
                            ]
                        },
                        {"name": "Business Intelligence", "value": 20}
                    ]
                }
            ]
        },
        {
            "name": "Marketing & Sales",
            "children": [
                {
                    "name": "Digital Marketing",
                    "children": [
                        {
                            "name": "Search Marketing",
                            "children": [
                                {"name": "SEO", "value": 25},
                                {"name": "Google Ads", "value": 20},
                                {"name": "Bing Ads", "value": 8}
                            ]
                        },
                        {
                            "name": "Social Media",
                            "children": [
                                {"name": "Facebook/Meta", "value": 18},
                                {"name": "LinkedIn", "value": 15},
                                {"name": "Twitter/X", "value": 10},
                                {"name": "TikTok", "value": 12},
                                {"name": "YouTube", "value": 15}
                            ]
                        },
                        {
                            "name": "Content Marketing",
                            "children": [
                                {"name": "Blog Content", "value": 20},
                                {"name": "Video Content", "value": 25},
                                {"name": "Podcasts", "value": 12},
                                {"name": "Email Marketing", "value": 18}
                            ]
                        }
                    ]
                },
                {
                    "name": "Sales Operations",
                    "children": [
                        {
                            "name": "B2B Sales",
                            "children": [
                                {"name": "Enterprise", "value": 40},
                                {"name": "Mid-Market", "value": 30},
                                {"name": "SMB", "value": 25}
                            ]
                        },
                        {
                            "name": "B2C Sales",
                            "children": [
                                {"name": "E-commerce", "value": 35},
                                {"name": "Retail", "value": 25},
                                {"name": "Direct Sales", "value": 15}
                            ]
                        },
                        {"name": "Customer Success", "value": 30},
                        {"name": "Sales Enablement", "value": 20}
                    ]
                },
                {
                    "name": "Brand & Creative",
                    "children": [
                        {"name": "Brand Strategy", "value": 25},
                        {"name": "Graphic Design", "value": 30},
                        {"name": "UX/UI Design", "value": 35},
                        {"name": "Photography", "value": 15},
                        {"name": "Video Production", "value": 20}
                    ]
                }
            ]
        },
        {
            "name": "Operations",
            "children": [
                {
                    "name": "Human Resources",
                    "children": [
                        {
                            "name": "Talent Acquisition",
                            "children": [
                                {"name": "Technical Recruiting", "value": 25},
                                {"name": "Sales Recruiting", "value": 20},
                                {"name": "Executive Search", "value": 15}
                            ]
                        },
                        {"name": "Employee Development", "value": 30},
                        {"name": "Compensation & Benefits", "value": 25},
                        {"name": "HR Operations", "value": 20}
                    ]
                },
                {
                    "name": "Finance & Accounting",
                    "children": [
                        {"name": "Financial Planning", "value": 30},
                        {"name": "Accounting", "value": 25},
                        {"name": "Tax & Compliance", "value": 20},
                        {"name": "Investor Relations", "value": 15}
                    ]
                },
                {
                    "name": "Legal & Compliance",
                    "children": [
                        {"name": "Corporate Law", "value": 20},
                        {"name": "IP & Patents", "value": 15},
                        {"name": "Privacy & Data", "value": 18},
                        {"name": "Contracts", "value": 22}
                    ]
                },
                {
                    "name": "Facilities & Admin",
                    "children": [
                        {"name": "Office Management", "value": 15},
                        {"name": "IT Support", "value": 20},
                        {"name": "Security", "value": 18},
                        {"name": "Procurement", "value": 12}
                    ]
                }
            ]
        },
        {
            "name": "Product",
            "children": [
                {
                    "name": "Product Management",
                    "children": [
                        {"name": "Product Strategy", "value": 30},
                        {"name": "Product Analytics", "value": 25},
                        {"name": "Roadmap Planning", "value": 20},
                        {"name": "User Research", "value": 25}
                    ]
                },
                {
                    "name": "Design",
                    "children": [
                        {
                            "name": "User Experience",
                            "children": [
                                {"name": "UX Research", "value": 20},
                                {"name": "Information Architecture", "value": 15},
                                {"name": "Interaction Design", "value": 18}
                            ]
                        },
                        {
                            "name": "User Interface",
                            "children": [
                                {"name": "Visual Design", "value": 22},
                                {"name": "Design Systems", "value": 18},
                                {"name": "Prototyping", "value": 15}
                            ]
                        }
                    ]
                },
                {
                    "name": "Quality Assurance",
                    "children": [
                        {"name": "Manual Testing", "value": 20},
                        {"name": "Automation Testing", "value": 25},
                        {"name": "Performance Testing", "value": 15},
                        {"name": "Security Testing", "value": 12}
                    ]
                }
            ]
        }
    ]
}

# Global state variables
original_data = sample_data
current_root = sample_data
zoom_history = [sample_data]
current_wedges = []
plot = None
source = None
center_source = None
title_div = None
width = 700
height = 700
radius = min(width, height) // 3

def get_node_value(node: Dict) -> float:
    """Get the total value of a node"""
    if 'value' in node:
        return node['value']
    elif 'children' in node:
        return sum(get_node_value(child) for child in node['children'])
    return 1
def lighten(hex_color, factor=0.5):
    """Return lighter hex color. factor in [0,1], higher is lighter."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    lighten_rgb = tuple(int((1-factor)*c + factor*255) for c in rgb)
    return '#{:02x}{:02x}{:02x}'.format(*lighten_rgb)

def build_full_sunburst(root_node: Dict) -> List[Dict]:
    """
    Sunburst: top-level = PALETTE, descendants = shade of their parent's color.
    """
    wedges = []
    max_depth = 5

    def process_node(node, depth, start_angle, end_angle, parent_color, color_index):
        # Pick color for this wedge
        if depth == 1:
            # First ring: assign from palette (by order)
            this_color = PALETTE[color_index % len(PALETTE)]
        elif depth > 1:
            # Descendants: shade the parent color lighter each level
            this_color = shade(parent_color, factor=min(0.1*depth, 0.9))
        else:
            this_color = None  # root itself isn't a wedge

        if depth > 0:
            inner_r = 30 + (depth - 1) * 60
            outer_r = 30 + depth * 60
            wedges.append({
                'name': node['name'],
                'value': get_node_value(node),
                'depth': depth,
                'start_angle': start_angle,
                'end_angle': end_angle,
                'inner_radius': inner_r,
                'outer_radius': outer_r,
                'has_children': bool(node.get('children')),
                'node_data': node,
                'parent_name': "",  # optional for legend
                'color': this_color,
                'color_index': color_index,
            })

        # Recurse children
        if node.get('children'):
            children = node['children']
            total_value = sum(get_node_value(child) for child in children)
            cur_angle = start_angle
            for i, child in enumerate(children):
                child_value = get_node_value(child)
                proportion = child_value / total_value if total_value else 0
                span = (end_angle - start_angle) * proportion
                next_angle = cur_angle + span
                # Children of root: color_index = i (to cycle palette)
                if depth == 0:
                    process_node(child, depth+1, cur_angle, next_angle, PALETTE[i % len(PALETTE)], i)
                else:
                    process_node(child, depth+1, cur_angle, next_angle, this_color, color_index)
                cur_angle = next_angle

    process_node(root_node, 0, 0, 2 * math.pi, None, -1)
    return wedges
def build_single_level(root_node: Dict) -> List[Dict]:
    """Build single level view for zoomed state, using legend palette for color"""
    wedges = []

    from bokeh.palettes import Category10
    PALETTE = Category10[10]

    if not root_node.get('children'):
        return wedges

    children = root_node.get('children', [])
    total_value = sum(get_node_value(child) for child in children)

    if total_value == 0:
        return wedges

    current_angle = 0

    for i, child in enumerate(children):
        child_value = get_node_value(child)
        proportion = child_value / total_value
        child_span = proportion * 2 * math.pi
        child_end = current_angle + child_span

        # Single ring that fills most of the space
        inner_r = radius * 0.2
        outer_r = radius * 0.9

        wedge = {
            'name': child['name'],
            'value': child_value,
            'depth': 1,
            'start_angle': current_angle,
            'end_angle': child_end,
            'inner_radius': inner_r,
            'outer_radius': outer_r,
            'has_children': bool(child.get('children')),
            'node_data': child,
            'parent_name': root_node['name'],
            'color_index': i,
            'color': PALETTE[i % len(PALETTE)],  # <<<<<< Add this line!
        }

        wedges.append(wedge)
        current_angle = child_end

    return wedges

def create_plot():
    """Create the Bokeh plot"""
    p = figure(
        width=width, 
        height=height,
        title="",  # We'll use the div for title now
        toolbar_location="above",
        x_range=(-radius*1.3, radius*1.3),
        y_range=(-radius*1.3, radius*1.3),
        tools="pan,wheel_zoom,reset"
    )
    
    # Style the plot
    p.axis.visible = False
    p.grid.visible = False
    p.outline_line_color = None
    p.background_fill_color = "#fafafa"
    
    return p

def zoom_to_node(node_data: Dict):
    """Zoom into a specific node"""
    global current_root, zoom_history
    
    print(f"ZOOM IN: {node_data['name']}")
    zoom_history.append(node_data)
    current_root = node_data
    update_chart()

def zoom_back():
    """Go back to parent level"""
    global current_root, zoom_history
    
    if len(zoom_history) > 1:
        old_name = current_root['name']
        zoom_history.pop()
        current_root = zoom_history[-1]
        print(f"ZOOM OUT: {old_name} -> {current_root['name']}")
        update_chart()
    else:
        print("Already at root level")

def handle_selection(attr, old, new):
    """Handle wedge selection"""
    global current_wedges
    
    if hasattr(handle_selection, '_updating'):
        return
        
    if new and len(new) > 0:
        selected_idx = new[0]
        if selected_idx < len(current_wedges):
            wedge = current_wedges[selected_idx]
            if wedge['has_children']:
                print(f"Zooming into: {wedge['name']}")
                zoom_to_node(wedge['node_data'])
            else:
                print(f"Clicked on leaf node: {wedge['name']} (no children)")
                
            # Clear selection
            handle_selection._updating = True
            source.selected.indices = []
            delattr(handle_selection, '_updating')

def handle_center_click(attr, old, new):
    """Handle center circle click"""
    if new and len(new) > 0:
        print("Clicked center - going back")
        zoom_back()
        center_source.selected.indices = []

def get_parent_colors(root_node):
    if not root_node.get("children"):
        return {}
    return {child["name"]: PALETTE[i % len(PALETTE)] for i, child in enumerate(root_node["children"])}

def prepare_wedge_data(wedges: List[Dict]) -> Dict[str, List]:
    data = {
        'x': [],
        'y': [],
        'start_angle': [],
        'end_angle': [],
        'inner_radius': [],
        'outer_radius': [],
        'name': [],
        'value': [],
        'color': [],
        'alpha': [],
        'line_alpha': [],
        'has_children': [],
        'node_index': []
    }
    for i, wedge in enumerate(wedges):
        data['x'].append(0)
        data['y'].append(0)
        data['start_angle'].append(wedge['start_angle'])
        data['end_angle'].append(wedge['end_angle'])
        data['inner_radius'].append(wedge['inner_radius'])
        data['outer_radius'].append(wedge['outer_radius'])
        data['name'].append(wedge['name'])
        data['value'].append(int(wedge['value']))
        data['has_children'].append(wedge['has_children'])
        data['node_index'].append(i)
        data['color'].append(wedge['color'])
        data['alpha'].append(0.85 if wedge['has_children'] else 0.65)
        data['line_alpha'].append(1.0)
    return data


def shade(hex_color, factor=0.2):
    """
    Lighten color by factor (0=no change, 1=white).
    factor can also be negative for darkening.
    """
    hex_color = hex_color.lstrip('#')
    rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    def clamp(x): return int(max(0, min(x, 255)))
    if factor >= 0:
        rgb = [clamp(c + (255 - c) * factor) for c in rgb]
    else:
        rgb = [clamp(c * (1 + factor)) for c in rgb]
    return '#%02x%02x%02x' % tuple(rgb)

def create_legend_div_for_parents(parent_colors, root_node):
    if not root_node.get("children"):
        return Div(text="<b>No children</b>", width=300)
    items = []
    for c in root_node["children"]:
        color = parent_colors.get(c["name"], "#cccccc")
        name = c["name"]
        value = get_node_value(c)
        items.append(
            f"<span style='display:inline-block; width:1.4em; text-align:center; color:{color}; font-size:1.3em'>■</span> "
            f"<span style='font-weight:600;'>{name}</span> "
            f"<span style='color:#666;'>({value})</span>"
        )
    legend_html = "<div style='padding:8px;'><b>Legend:</b><br>" + "<br>".join(items) + "</div>"
    return Div(text=legend_html, width=300, styles={"overflow-y": "auto"})

def update_chart():
    global current_wedges, source, center_source, title_div, legend_div

    parent_colors = get_parent_colors(current_root)
    is_at_root = len(zoom_history) <= 1
    show_full = is_at_root

    wedges = build_full_sunburst(current_root) if show_full else build_single_level(current_root)
    current_wedges = wedges
    new_data = prepare_wedge_data(wedges)
    source.data = new_data

    legend_div.text = create_legend_div_for_parents(parent_colors, current_root).text


    # --- (rest of your function unchanged) ---
    if len(zoom_history) <= 1:
        center_source.data = dict(x=[0], y=[0], radius=[0])  # Hide
    else:
        center_source.data = dict(x=[0], y=[0], radius=[25])  # Show
        
    breadcrumb = " > ".join([h['name'] for h in zoom_history])
    if len(zoom_history) == 1:
        title_text = f"<h2 style='text-align: center; margin: 10px;'>{current_root['name']}</h2>"
    else:
        title_text = f"<h2 style='text-align: center; margin: 10px;'>{breadcrumb}</h2>"
    title_div.text = title_text

    view_type = "full sunburst" if show_full else "single level"
    print(f"Updated chart with {len(wedges)} wedges for '{current_root['name']}' ({view_type})")
    if wedges:
        clickable = sum(1 for w in wedges if w['has_children'])
        print(f"  - {clickable} segments are clickable (have children)")

def modify_doc(doc):
    """Create the Bokeh application with always-updating legend."""
    global plot, source, center_source, title_div, legend_div
    
    title_div = Div(
        text=f"<h2 style='text-align: center; margin: 10px;'>{sample_data['name']}</h2>",
        width=width,
        height=30
    )
    
    legend_div = Div(text="", width=300, height=300, styles={"overflow-y": "auto"})
    
    plot = create_plot()
    source = ColumnDataSource()
    center_source = ColumnDataSource(dict(x=[0], y=[0], radius=[0]))
    
    wedge_renderer = plot.annular_wedge(
        x='x', y='y',
        inner_radius='inner_radius', outer_radius='outer_radius',
        start_angle='start_angle', end_angle='end_angle',
        color='color', alpha='alpha',
        line_color='white', line_width=3, line_alpha='line_alpha',
        source=source,
        selection_fill_alpha=1.0,
        nonselection_fill_alpha=0.7,
        hover_fill_alpha=0.9,
        hover_line_color='black',
        hover_line_width=4
    )
    
    center_circle = plot.circle(
        x='x', y='y', radius='radius', 
        color='lightblue', alpha=0.8, 
        line_color='darkblue', line_width=4,
        source=center_source,
        hover_color='blue',
        hover_alpha=1.0,
        selection_color='darkblue'
    )
    
    hover = HoverTool(
        tooltips=[
            ("Name", "@name"),
            ("Value", "@value{,0}"),
            ("Clickable", "@has_children")
        ],
        renderers=[wedge_renderer]
    )
    plot.add_tools(hover)
    
    tap = TapTool()
    plot.add_tools(tap)
    
    source.selected.on_change('indices', handle_selection)
    center_source.selected.on_change('indices', handle_center_click)
    
    legend_div = Div(text="", width=300, height=300, styles={"overflow-y": "auto"})

    update_chart()  # This will also update the legend
    
    layout = row(
        column(title_div, row(plot,legend_div)),
        
    )
    doc.add_root(layout)
    doc.title = "Animated Zoomable Sunburst Chart"

# For running as a script
if __name__ == "__main__":
    from bokeh.application import Application
    from bokeh.application.handlers import FunctionHandler
    from bokeh.server.server import Server

    app = Application(FunctionHandler(modify_doc))
    server = Server({'/': app}, num_procs=1, port=5006)
    server.start()
    print("Opening Bokeh application on http://localhost:5006/")
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
