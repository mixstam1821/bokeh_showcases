# my post: https://discourse.bokeh.org/t/rounded-doughnut-chart/12535

import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool

def rounded_annular_wedge_patch(center, inner_radius, outer_radius, start_angle, end_angle, 
                               corner_radius=0.05, n_points=80, gap_width=0):
    cx, cy = center
    if gap_width > 0:
        inner_gap_angle = gap_width / inner_radius / 2.5
        outer_gap_angle = gap_width / outer_radius / 2
        start_angle_inner = start_angle + inner_gap_angle
        end_angle_inner = end_angle - inner_gap_angle
        start_angle_outer = start_angle + outer_gap_angle  
        end_angle_outer = end_angle - outer_gap_angle
    else:
        start_angle_inner = start_angle_outer = start_angle
        end_angle_inner = end_angle_outer = end_angle
    corner_points = 15
    angular_corner_offset_inner = corner_radius / inner_radius
    angular_corner_offset_outer = corner_radius / outer_radius
    outer_start_adj = start_angle_outer + angular_corner_offset_outer
    outer_end_adj = end_angle_outer - angular_corner_offset_outer
    if outer_end_adj > outer_start_adj:
        outer_angles = np.linspace(outer_start_adj, outer_end_adj, n_points)
        x_outer = cx + outer_radius * np.cos(outer_angles)
        y_outer = cy + outer_radius * np.sin(outer_angles)
    else:
        x_outer = np.array([])
        y_outer = np.array([])
    inner_start_adj = end_angle_inner - angular_corner_offset_inner
    inner_end_adj = start_angle_inner + angular_corner_offset_inner
    if inner_start_adj > inner_end_adj:
        inner_angles = np.linspace(inner_start_adj, inner_end_adj, n_points)
        x_inner = cx + inner_radius * np.cos(inner_angles)
        y_inner = cy + inner_radius * np.sin(inner_angles)
    else:
        x_inner = np.array([])
        y_inner = np.array([])
    # Corners
    corner1_center_x = cx + (outer_radius - corner_radius) * np.cos(start_angle_outer)
    corner1_center_y = cy + (outer_radius - corner_radius) * np.sin(start_angle_outer)
    c1_start = start_angle_outer - np.pi/2
    c1_end = start_angle_outer
    c1_angles = np.linspace(c1_start, c1_end, corner_points)
    x_c1 = corner1_center_x + corner_radius * np.cos(c1_angles)
    y_c1 = corner1_center_y + corner_radius * np.sin(c1_angles)
    corner2_center_x = cx + (outer_radius - corner_radius) * np.cos(end_angle_outer)
    corner2_center_y = cy + (outer_radius - corner_radius) * np.sin(end_angle_outer)
    c2_start = end_angle_outer
    c2_end = end_angle_outer + np.pi/2
    c2_angles = np.linspace(c2_start, c2_end, corner_points)
    x_c2 = corner2_center_x + corner_radius * np.cos(c2_angles)
    y_c2 = corner2_center_y + corner_radius * np.sin(c2_angles)
    corner3_center_x = cx + (inner_radius + corner_radius) * np.cos(end_angle_inner)
    corner3_center_y = cy + (inner_radius + corner_radius) * np.sin(end_angle_inner)
    c3_start = end_angle_inner + np.pi/2
    c3_end = end_angle_inner + np.pi
    c3_angles = np.linspace(c3_start, c3_end, corner_points)
    x_c3 = corner3_center_x + corner_radius * np.cos(c3_angles)
    y_c3 = corner3_center_y + corner_radius * np.sin(c3_angles)
    corner4_center_x = cx + (inner_radius + corner_radius) * np.cos(start_angle_inner)
    corner4_center_y = cy + (inner_radius + corner_radius) * np.sin(start_angle_inner)
    c4_start = start_angle_inner + np.pi
    c4_end = start_angle_inner + 3*np.pi/2
    c4_angles = np.linspace(c4_start, c4_end, corner_points)
    x_c4 = corner4_center_x + corner_radius * np.cos(c4_angles)
    y_c4 = corner4_center_y + corner_radius * np.sin(c4_angles)
    x_patch = np.concatenate([
        x_c1, x_outer, x_c2, x_c3, x_inner, x_c4
    ])
    y_patch = np.concatenate([
        y_c1, y_outer, y_c2, y_c3, y_inner, y_c4
    ])
    return x_patch, y_patch

def plot_rounded_annular_wedges(
    data, labels=None, colors=None, center=(0,0),
    inner_radius=0.5, outer_radius=1.0, corner_radius=0.08, gap_width=0.19, n_points=80,
    title="Rounded Doughnut Chart"
):
    total = sum(data)
    N = len(data)
    if not colors:
        colors = ["gold", "lime", "dodgerblue", "purple", "orange", "cyan", "magenta"]
    colors = (colors * ((N + len(colors) - 1) // len(colors)))[:N]
    if not labels:
        labels = [f"Piece {i+1}" for i in range(N)]
    angles = [2*np.pi*v/total for v in data]
    start_angle = np.deg2rad(30)
    starts = [start_angle]
    for a in angles[:-1]:
        starts.append(starts[-1] + a)
    ends = [s + a for s, a in zip(starts, angles)]
    percents = [f"{int(round(100 * v / total))}%" for v in data]

    xs, ys = [], []
    for s, e in zip(starts, ends):
        x, y = rounded_annular_wedge_patch(
            center, inner_radius, outer_radius, s, e, corner_radius, n_points, gap_width=gap_width
        )
        xs.append(x.tolist())
        ys.append(y.tolist())

    source = ColumnDataSource(data=dict(
        xs=xs, ys=ys, label=labels, percent=percents, color=colors
    ))

    p = figure(width=550, height=420, x_range=(-1.3, 2.3), y_range=(-1.3, 1.3),
               match_aspect=True, title=title)
    patches_renderer = p.patches('xs', 'ys', source=source,
                                 fill_color='color', fill_alpha=0.7,
                                 line_color="white", line_width=2,
                                 hover_line_color='black', hover_line_width=3)

    hover = HoverTool(
        tooltips=[("Label", "@label"), ("Percent", "@percent")],
        renderers=[patches_renderer]
    )
    p.add_tools(hover)

    # Percentage text labels
    label_coords_x = []
    label_coords_y = []
    for s, e in zip(starts, ends):
        mid_angle = (s + e) / 2
        r_label = (inner_radius + outer_radius) / 2
        lx = center[0] + r_label * np.cos(mid_angle)
        ly = center[1] + r_label * np.sin(mid_angle)
        label_coords_x.append(lx)
        label_coords_y.append(ly)

    p.text(
        x=label_coords_x,
        y=label_coords_y,
        text=percents,
        text_align="center",
        text_baseline="middle",
        text_font_size="14pt",
        text_color="black",
        text_font_style="bold"
    )

    # Custom legend (top right)
    legend_x = 1.22
    legend_y = 0.8
    legend_spacing = 0.16
    for i, (c, lbl) in enumerate(zip(colors, labels)):
        y_pos = legend_y - i * legend_spacing
        p.scatter([legend_x], [y_pos], size=18, color=c, alpha=0.7)
        p.text([legend_x + 0.09], [y_pos], text=[lbl], text_align="left", text_baseline="middle", text_font_size="13pt")

    p.grid.visible = False
    p.axis.visible = False
    p.title.text_font_size = "17pt"
    p.title.align = "center"
    p.background_fill_color="#fff9e5" 
    show(p)

# ----- Example Usage -----
data = [10, 15, 5, 12, 18]
labels = ["Apples", "Pears", "Bananas", "Plums", "Tomatoes"]
colors = ["gold", "lime", "dodgerblue", "purple", "tomato"]

plot_rounded_annular_wedges(
    data, labels=labels, colors=colors,
    inner_radius=0.5, outer_radius=1.0,
    corner_radius=0.08, gap_width=0.19
)


data3 = [7, 13, 15, 5, 3, 9]
labels3 = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Weekend"]
colors3 = ["#f67280", "#ffafcc", "#a3cef1", "#b5ead7", "#f6ffe0", "#d2f6c5"]

plot_rounded_annular_wedges(
    data3, labels=labels3, colors=colors3,
    inner_radius=0.5, outer_radius=1,
    corner_radius=0.08, gap_width=0.19,
    title="Weekly Activity",
)




data2 = [25, 15, 35, 25]
labels2 = ["HR", "R&D", "Marketing", "Sales"]
colors2 = ["#5e60ce", "#00b4d8", "#ffd166", "#ff006e"]

plot_rounded_annular_wedges(
    data2, labels=labels2, colors=colors2,
    inner_radius=0.5, outer_radius=1.0,
    corner_radius=0.08, gap_width=0.19,
    title="Department Budgets",
)
