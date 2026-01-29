"""
SurfaceGlobe - High-level Bokeh widget for gridded data visualization
"""
from bokeh.core.properties import Bool, Float, Int, List, String, Any
from bokeh.models import LayoutDOM
import numpy as np


class SurfaceGlobe(LayoutDOM):
    """
    High-level widget for visualizing gridded data on sphere or map projections.
    
    Example:
        globe = SurfaceGlobe(
            lons=lons_flat,
            lats=lats_flat,
            values=temps_flat,
            n_lat=30,
            n_lon=60,
            projection='sphere',
            palette='Turbo256',
            autorotate=True
        )
        show(globe)
    """
    
    __implementation__ = "surface_globe.ts"
    
    # Data
    lons = List(Float, default=[], help="Flattened longitude array (or X for surface_3d)")
    lats = List(Float, default=[], help="Flattened latitude array (or Y for surface_3d)")
    values = List(Float, default=[], help="Flattened values array (or Z for surface_3d)")
    n_lat = Int(default=30, help="Number of latitude/Y points")
    n_lon = Int(default=60, help="Number of longitude/X points")
    
    # Projection
    projection = String(default='sphere', help="'sphere', 'mollweide', 'natural_earth', 'plate_carree', or 'surface_3d'")
    
    # Color mapping
    palette = String(default='Turbo256', help="Palette name")
    vmin = Float(default=float('nan'), help="Min value for color scale")
    vmax = Float(default=float('nan'), help="Max value for color scale")
    nan_color = String(default='#808080', help="Color for NaN values")
    
    # View controls
    rotation = Float(default=0, help="Rotation angle (degrees) - works for all projections")
    tilt = Float(default=0, help="Tilt angle (degrees) - works for sphere and surface_3d")
    azimuth = Float(default=0, help="Azimuth angle (degrees)")
    zoom = Float(default=1.0, help="Zoom level")
    
    # Animation
    autorotate = Bool(default=False, help="Auto-rotate sphere")
    rotation_speed = Float(default=1.0, help="Rotation speed")
    
    # Coastlines
    show_coastlines = Bool(default=True, help="Show coastlines (for geographic projections)")
    coastline_color = String(default='#000000', help="Coastline color")
    coastline_width = Float(default=1.2, help="Coastline width")
    coast_lons = List(Any, default=[], help="Coastline longitudes")
    coast_lats = List(Any, default=[], help="Coastline latitudes")
    
    # Interaction
    enable_hover = Bool(default=True, help="Enable hover tooltip")


def create_globe(lons, lats, values, n_lat, n_lon,
                projection='sphere',
                palette='Turbo256',
                vmin=None, vmax=None,
                autorotate=False,
                show_coastlines=True,
                enable_hover=True,
                width=800, height=800):
    """
    High-level function to create a globe with coastlines.
    
    Args:
        lons: Flattened longitude array (or X values for surface_3d)
        lats: Flattened latitude array (or Y values for surface_3d)
        values: Flattened data values (or Z values for surface_3d)
        n_lat: Number of latitude/Y points
        n_lon: Number of longitude/X points
        projection: 'sphere', 'mollweide', 'natural_earth', 'plate_carree', or 'surface_3d'
        palette: Color palette name
        vmin: Min value for color scale (None = auto)
        vmax: Max value for color scale (None = auto)
        autorotate: Enable auto-rotation for sphere
        show_coastlines: Show coastline overlay (for geographic projections)
        enable_hover: Enable hover tooltip to show values
        width: Widget width
        height: Widget height
    
    Returns:
        SurfaceGlobe widget
    """
    
    # Load coastlines (only for geographic projections)
    coast_lons_data = []
    coast_lats_data = []
    
    if show_coastlines and projection != 'surface_3d':
        try:
            import cartopy.feature as cfeature
            from shapely.geometry import LineString, MultiLineString
            
            coastlines = cfeature.NaturalEarthFeature('physical', 'coastline', '110m')
            for geom in coastlines.geometries():
                if isinstance(geom, LineString):
                    coords = np.array(geom.coords)
                    coast_lons_data.extend(coords[:, 0].tolist() + [None])
                    coast_lats_data.extend(coords[:, 1].tolist() + [None])
                elif isinstance(geom, MultiLineString):
                    for line in geom.geoms:
                        coords = np.array(line.coords)
                        coast_lons_data.extend(coords[:, 0].tolist() + [None])
                        coast_lats_data.extend(coords[:, 1].tolist() + [None])
        except ImportError:
            print("Warning: cartopy not available")
            show_coastlines = False
    
    if vmin is None:
        vmin = float('nan')
    if vmax is None:
        vmax = float('nan')
    
    return SurfaceGlobe(
        lons=lons,
        lats=lats,
        values=values,
        n_lat=n_lat,
        n_lon=n_lon,
        projection=projection,
        palette=palette,
        vmin=vmin,
        vmax=vmax,
        autorotate=autorotate,
        show_coastlines=show_coastlines,
        coast_lons=coast_lons_data,
        coast_lats=coast_lats_data,
        enable_hover=enable_hover,
        width=width,
        height=height
    )


def create_surface(Z_func, x_range=(-3, 3), y_range=(-3, 3), n_points=40,
                   elev_deg=25, azim_deg=45, palette='Viridis256',
                   autorotate=False, title="3D Surface", width=800, height=800):
    """
    Create a 3D surface plot from a function Z(X, Y).
    
    Args:
        Z_func: Function that takes X, Y meshgrids and returns Z values
        x_range: (min, max) for X axis
        y_range: (min, max) for Y axis
        n_points: Resolution of grid
        elev_deg: Elevation angle in degrees (tilt)
        azim_deg: Azimuth angle in degrees (rotation)
        palette: Color palette name
        autorotate: Enable auto-rotation
        title: Plot title
        width: Widget width
        height: Widget height
    
    Returns:
        SurfaceGlobe widget configured as a 3D surface
    
    Example:
        >>> surface = create_surface(
        ...     lambda X, Y: np.sin(X) * np.cos(Y),
        ...     title="sin(X) * cos(Y)",
        ...     autorotate=True
        ... )
        >>> show(surface)
    """
    # Generate grid
    x = np.linspace(x_range[0], x_range[1], n_points)
    y = np.linspace(y_range[0], y_range[1], n_points)
    X, Y = np.meshgrid(x, y)
    Z = Z_func(X, Y)
    
    # Flatten
    x_flat = X.flatten().tolist()
    y_flat = Y.flatten().tolist()
    z_flat = Z.flatten().tolist()
    
    # Create and return the widget
    widget = create_globe(
        lons=x_flat,  # X values
        lats=y_flat,  # Y values
        values=z_flat,  # Z values
        n_lat=n_points,
        n_lon=n_points,
        projection='surface_3d',
        palette=palette,
        show_coastlines=False,
        width=width,
        height=height
    )
    
    # Set rotation, tilt, and autorotate
    widget.rotation = azim_deg
    widget.tilt = elev_deg
    widget.autorotate = autorotate
    
    return widget
