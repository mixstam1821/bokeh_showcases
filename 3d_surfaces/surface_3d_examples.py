"""
3D Surface Examples - Using SurfaceGlobe for mathematical surfaces
"""
import numpy as np
from bokeh.io import show, output_file
from bokeh.layouts import gridplot
from surface_globe import create_surface

# ============================================================
# EXAMPLE SURFACES
# ============================================================

best_surfaces = [
    (lambda X, Y: np.sin(X*2) * np.cos(Y*2), 
     "Smooth Wave Hills"),
    
    (lambda X, Y: np.sin(3*np.sqrt(X**2 + Y**2)) / (np.sqrt(X**2 + Y**2) + 1e-6), 
     "Circular Ripple"),
    
    (lambda X, Y: (1 - (X**2 + Y**2)) * np.exp(-(X**2 + Y**2)/2), 
     "Mexican Hat"),
    
    (lambda X, Y: np.sin(X) * np.cos(Y), 
     "sin(X) * cos(Y)"),
    
    (lambda X, Y: np.sin(np.sqrt(X**2 + Y**2)), 
     "sin(sqrt(X² + Y²))"),
    
    (lambda X, Y: np.exp(-0.1*(X**2 + Y**2)) * np.sin(X*2) * np.cos(Y*2), 
     "Damped Sine-Cosine"),
    
    (lambda X, Y: np.tanh(X) * np.tanh(Y), 
     "tanh(X) * tanh(Y)"),
    
    (lambda X, Y: np.sin(X) * np.sin(Y) + np.cos(X*Y), 
     "sin(X)sin(Y) + cos(XY)"),
]

# Create surfaces
surfaces = []
for idx, (func, name) in enumerate(best_surfaces, 1):
    print(f"Creating surface {idx}: {name}")
    
    surface = create_surface(
        Z_func=func,
        x_range=(-3, 3),
        y_range=(-3, 3),
        n_points=40,
        elev_deg=25,
        azim_deg=45,
        palette='Viridis256',
        title=f"Surface {idx}: {name}",
        width=600,
        height=500
    )
    
    surfaces.append(surface)
    
    # Save individual files
    output_file(f"surface_best_{idx}.html")
    show(surface)

# Create a grid of all surfaces
print("\nCreating combined grid...")
grid = gridplot(
    [surfaces[i:i+2] for i in range(0, len(surfaces), 2)],
    toolbar_location=None
)

output_file("all_surfaces.html")
show(grid)

print("""
✨ 3D Surface Viewer Created!
=============================
Features:
- Drag to rotate the surface
- Mouse wheel to zoom
- Tilt slider to change elevation
- Rotation slider to spin around

All surfaces are interactive - try dragging them!
""")
