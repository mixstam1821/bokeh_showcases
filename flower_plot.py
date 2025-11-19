# see my post here: https://discourse.bokeh.org/t/custom-plot-flower/12639

import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot
from bokeh.models import Label
from bokeh.palettes import all_palettes

def flower(
    data_values,
    labels,
    title="Sunflower",
    palette="YlOrBr",      # palette name or list of hex strings
    n_layers=6,
    show_data=0,           # 0: labels only, 1: labels + values
    fontlabel="13pt",
    center_radius=0.4,
    figsize=350,
    color_mode="uniform",  # "uniform" | "by_value"
    gradient_to="#FFFFFF"  # fade target for "by_value"
):
    # ---------------------------
    # Normalize safely
    # ---------------------------
    data_values = np.array(data_values)
    n_petals = len(data_values)
    vmin, vmax = float(data_values.min()), float(data_values.max())
    normalized_vals = np.ones_like(data_values, dtype=float) if vmax == vmin \
        else (data_values - vmin) / (vmax - vmin)

    # ---------------------------
    # Resolve palette
    # ---------------------------
    if isinstance(palette, str):
        if palette in all_palettes:
            palette = all_palettes[palette][max(all_palettes[palette].keys())]
        else:
            raise ValueError(f"Unknown palette '{palette}'. Try e.g. 'Viridis', 'Inferno', 'Turbo'.")
    palette = list(palette)

    # ---------------------------
    # Color helpers
    # ---------------------------
    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def lerp_hex(c1, c2, t):
        r1, g1, b1 = hex_to_rgb(c1)
        r2, g2, b2 = hex_to_rgb(c2)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def get_interpolated_color(pal, value):
        """Smooth color interpolation across the palette."""
        value = max(0.0, min(1.0, float(value)))
        pos = value * (len(pal) - 1)
        i0 = int(np.floor(pos))
        i1 = min(i0 + 1, len(pal) - 1)
        t = pos - i0
        return lerp_hex(pal[i0], pal[i1], t)

    def gradient_from_palette(pal, steps):
        """Make a smooth gradient spanning the entire palette."""
        if len(pal) == 1:
            return [lerp_hex(pal[0], gradient_to, j / (steps - 1)) for j in range(steps)]
        colors = []
        for j in range(steps):
            pos = j / (steps - 1)
            colors.append(get_interpolated_color(pal, pos))
        return colors

    # ---------------------------
    # Build layer colors
    # ---------------------------
    if color_mode == "uniform":
        # All petals share one same layered gradient across the full palette
        uniform_layers = gradient_from_palette(palette, n_layers)
    else:
        # by_value: each petal individually fades toward gradient_to
        uniform_layers = None

    # ---------------------------
    # Figure
    # ---------------------------
    max_petal_length = normalized_vals.max()
    plot_range = max_petal_length + center_radius + 2
    p = figure(
        width=figsize,
        height=figsize,
        title=title,
        x_range=(-plot_range, plot_range),
        y_range=(-plot_range, plot_range),
        toolbar_location=None,
        background_fill_color="#faf9f6",
    )
    p.grid.visible = False
    p.axis.visible = False
    p.title.text_font_size = "12pt"
    p.title.text_color = "#5d4630"
    p.title.align = "center"

    # ---------------------------
    # Petals
    # ---------------------------
    t = np.linspace(0, 2*np.pi, 60)
    for i in range(n_petals):
        angle_label = 2*np.pi * i / n_petals
        angle_petal = angle_label - np.pi/2
        petal_length = 0.6 + 0.9 * normalized_vals[i]
        petal_width  = 0.25 + 0.15 * petal_length

        x_local = petal_width * np.cos(t)
        y_local = petal_length * np.sin(t) + center_radius + petal_length
        x_petal = x_local * np.cos(angle_petal) - y_local * np.sin(angle_petal)
        y_petal = x_local * np.sin(angle_petal) + y_local * np.cos(angle_petal)

        # select color layers
        if color_mode == "uniform":
            layers = uniform_layers
            edge_color = layers[0]
        else:
            base = get_interpolated_color(palette, normalized_vals[i])
            layers = [lerp_hex(base, gradient_to, j / (n_layers - 1))
                      for j in range(n_layers)]
            edge_color = base

        # draw
        for j, col in enumerate(layers):
            scale = 1 - j * (0.7 / n_layers)
            alpha = 0.95 - j * 0.05
            x_scaled = x_petal * scale
            y_scaled = y_petal * scale
            p.patch(
                x_scaled, y_scaled,
                color=col, alpha=alpha,
                line_color=edge_color if j == 0 else col,
                line_width=2 if j == 0 else 0,
            )

        # labels
        offset = 0.3 + 0.1 * (petal_length / normalized_vals.max())
        label_distance = center_radius + 2 * petal_length + offset
        x_label = label_distance * np.cos(angle_label)
        y_label = label_distance * np.sin(angle_label)
        text = f"{labels[i]}\n{data_values[i]:.1f}" if show_data else labels[i]
        p.add_layout(Label(
            x=x_label, y=y_label,
            text=text,
            text_align="center", text_baseline="middle",
            text_font_size=fontlabel, text_font_style="bold",
            text_color="#654321",
        ))

    # expand range for labels
    pad = plot_range / 4
    p.x_range.start = -plot_range - pad
    p.x_range.end = plot_range + pad
    p.y_range.start = -plot_range - pad
    p.y_range.end = plot_range + pad

    # ---------------------------
    # Center disk + seeds
    # ---------------------------
    theta = np.linspace(0, 2*np.pi, 100)
    p.patch(center_radius*np.cos(theta), center_radius*np.sin(theta),
            color="#654321", alpha=0.95,
            line_color="#4a2f1a", line_width=2)

    rng = np.random.default_rng(42)
    for _ in range(65):
        ang = rng.uniform(0, 2*np.pi)
        r = rng.uniform(0, center_radius * 0.95)
        p.scatter(
            [r*np.cos(ang)], [r*np.sin(ang)],
            size=rng.uniform(2, 7),
            color="#4a2f1a", alpha=rng.uniform(0.5, 0.9)
        )

    return p




months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
solar  = [2.5, 3.5, 5.0, 6.5, 7.8, 8.5, 8.2, 7.0, 5.5, 4.0, 2.8, 2.2]

p = flower(
    data_values=solar,
    labels=months,
    title="Annual Solar Radiation (kWh/m²/day)",
    palette=['#FFD700'],
    show_data=1,
    figsize=1000

)
show(p)


p = flower(
    data_values=solar,
    labels=months,
    title="Annual Solar Radiation (kWh/m²/day)",
    palette="Viridis",
    color_mode="by_value",
    figsize=1000,
    show_data=1
)
show(p)



from bokeh.plotting import show, output_file

labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
values = [2.5, 3.4, 5.0, 6.5, 8.3, 8.8, 8.2, 7.1, 5.9, 4.0, 2.8, 2.1]

p = flower(
    data_values=values,
    labels=labels,
    title="Palette Gradient Sunflower",
    palette=[ '#FF7F00', '#FFFF00',  '#fc0afc'],        
    show_data=1,
    figsize=1000,
)
output_file("sunflower_palette_gradient.html")
show(p)


p = flower(
    data_values=values,
    labels=labels,
    title="Palette Gradient Sunflower",
    palette=[ '#FF7F00', '#FFFF00',  '#fc0afc'],        
    show_data=1,
    figsize=1000,
    color_mode="by_value",
)
output_file("sunflower_palette_gradient.html")
show(p)




skills = ['Python', 'SQL', 'Machine Learning', 'Visualization',
          'DE', 'APIs', 'Linux', 'Communication']

skill_scores = [9, 7, 8, 9, 6, 8, 7, 10]

p = flower(
    data_values=skill_scores,
    labels=skills,
    title="Developer Skill Profile (Self-assessment (1–10))",
    palette=[ '#74faff', '#ff61ff', '#ffe285', '#ff6161'],
    figsize=1000
)
output_file("sunflower_skills.html")
show(p)
