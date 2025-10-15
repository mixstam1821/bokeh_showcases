# https://discourse.bokeh.org/t/contourf-on-maps-with-custom-projection/12611
# A high-level Bokeh function to plot Contourf on Maps with custom Projection! 

from cartopy import crs as ccrs
from bokeh.plotting import figure, curdoc, show

def contourf_map(da, title=None,
                          levels=10,
                          palette="Viridis256",
                          vmin=None, vmax=None,
                          width=1500, height=780,
                          show_coastlines=True,
                          coastline_color='black',
                          coastline_width=1.5,
                          projection=None,
                          cbar_title=None,
                          sh=1):
    """
    Plot XArray DataArray with filled contours using Bokeh's native contour method.
    
    Supports various cartopy projections (Mollweide, Robinson, EqualEarth, EckertIV, Orthographic, Sinusoidal, Miller, AlbersEqualArea, PlateCarree) with proper handling of coordinate transformations,
    longitude wrapping for Orthographic projections, and coastline rendering without artifacts.
    
    Parameters
    ----------
    da : xarray.DataArray
        2D DataArray with latitude/longitude dimensions. Dimension names should contain
        'lat' and 'lon' (case-insensitive).
    title : str, optional
        Plot title. Default is None.
    levels : int or array-like, default=10
        Number of contour levels (if int) or explicit level values (if array-like).
    palette : str or list, default="Viridis256"
        Bokeh color palette name ("Viridis256", "Turbo256", "Plasma256", "Inferno256", 
        "Magma256") or list of color hex codes.
    vmin, vmax : float, optional
        Min/max values for color mapping. If None, uses data min/max.
    width, height : int, default=(1500, 780)
        Figure dimensions in pixels.
    show_coastlines : bool, default=True
        Whether to overlay coastlines from Natural Earth data.
    coastline_color : str, default='black'
        Color of coastline borders.
    coastline_width : float, default=1.5
        Width of coastline borders in pixels.
    projection : cartopy.crs projection, optional
        Cartopy projection (e.g., ccrs.Orthographic(), ccrs.Robinson()). 
        If None, uses PlateCarree (equirectangular).
    cbar_title : str, optional
        Title for the colorbar. Default is None.
    sh : int, default=1
        Show (sh=1) or not.
    """
    from shapely.geometry import LineString, MultiLineString
    import cartopy.feature as cfeature
    
    from bokeh.models import GlobalInlineStyleSheet
    gstyle = GlobalInlineStyleSheet(css=""" html, body, .bk, .bk-root {background-color: #343838; margin: 0; padding: 0; height: 100%; color: white; font-family: 'Consolas', 'Courier New', monospace; } .bk { color: white; } .bk-input, .bk-btn, .bk-select, .bk-slider-title, .bk-headers, .bk-label, .bk-title, .bk-legend, .bk-axis-label { color: white !important; } .bk-input::placeholder { color: #aaaaaa !important; } """)


    # Get data
    if da.ndim != 2:
        raise ValueError(f"DataArray must be 2D, got {da.ndim}D")
    
    arr = da.values.copy()
    lat_name = [dim for dim in da.dims if "lat" in dim.lower()][0]
    lon_name = [dim for dim in da.dims if "lon" in dim.lower()][0]
    lats = da[lat_name].values
    lons = da[lon_name].values
    
    # Set up projection
    if projection is None:
        projection = ccrs.PlateCarree()
        use_projection = False
    else:
        use_projection = True
    
    # Create meshgrid for contour
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    # CRITICAL FIX: Handle longitude wrapping ONLY for Orthographic projection
    # Orthographic needs this to avoid seam artifacts at ±180°
    if use_projection and isinstance(projection, ccrs.Orthographic):
        if not np.isclose(lon_grid[0, 0], lon_grid[0, -1], atol=1.0):
            # Check if this looks like global data (spans most of globe)
            lon_span = np.max(lons) - np.min(lons)
            if lon_span > 300:  # Likely global data
                # Add wrapped column at the end
                lon_grid = np.hstack([lon_grid, lon_grid[:, 0:1]])
                lat_grid = np.hstack([lat_grid, lat_grid[:, 0:1]])
                arr = np.hstack([arr, arr[:, 0:1]])
    
    # Transform coordinates if using projection
    if use_projection:
        transformed_points = projection.transform_points(ccrs.PlateCarree(), lon_grid, lat_grid)
        x_grid = transformed_points[:, :, 0]
        y_grid = transformed_points[:, :, 1]
        
        # CRITICAL FIX: Mask invalid transformed points
        # Points that are NaN, infinite, or have very large values are not visible
        invalid_mask = (np.isnan(x_grid) | np.isnan(y_grid) | 
                       np.isinf(x_grid) | np.isinf(y_grid) |
                       (np.abs(x_grid) > 1e10) | (np.abs(y_grid) > 1e10))
        
        # Set invalid points to NaN in both coordinates AND data
        x_grid[invalid_mask] = np.nan
        y_grid[invalid_mask] = np.nan
        arr[invalid_mask] = np.nan
        
        # Additional check: for orthographic projections, filter points too far from center
        # This helps with edge artifacts
        if isinstance(projection, ccrs.Orthographic):
            center_lon = projection.proj4_params.get('lon_0', 0)
            center_lat = projection.proj4_params.get('lat_0', 0)
            
            # Calculate angular distance from center
            from numpy import sin, cos, arccos, deg2rad
            lat_rad = deg2rad(lat_grid)
            lon_rad = deg2rad(lon_grid)
            center_lat_rad = deg2rad(center_lat)
            center_lon_rad = deg2rad(center_lon)
            
            # Great circle distance
            angular_dist = arccos(np.clip(
                sin(center_lat_rad) * sin(lat_rad) + 
                cos(center_lat_rad) * cos(lat_rad) * cos(lon_rad - center_lon_rad),
                -1, 1
            ))
            
            # Mask points beyond 90 degrees (not visible on hemisphere)
            beyond_horizon = angular_dist > np.pi / 2
            x_grid[beyond_horizon] = np.nan
            y_grid[beyond_horizon] = np.nan
            arr[beyond_horizon] = np.nan
    else:
        x_grid = lon_grid
        y_grid = lat_grid
    
    # Set up contour levels
    if vmin is None:
        vmin = np.nanmin(arr)
    if vmax is None:
        vmax = np.nanmax(arr)
    
    if isinstance(levels, int):
        level_values = np.linspace(vmin, vmax, levels)
    else:
        level_values = np.array(levels)
    
    # Get color palette
    if isinstance(palette, str):
        from bokeh.palettes import Viridis256, Turbo256, Plasma256, Inferno256, Magma256
        palette_map = {
            "Viridis256": Viridis256,
            "Turbo256": Turbo256,
            "Plasma256": Plasma256,
            "Inferno256": Inferno256,
            "Magma256": Magma256
        }
        palette_obj = palette_map.get(palette, Viridis256)
    else:
        palette_obj = palette
    
    # Sample colors from palette to match number of levels
    n_colors = len(level_values) - 1
    if len(palette_obj) > n_colors:
        indices = np.linspace(0, len(palette_obj) - 1, n_colors).astype(int)
        fill_palette = [palette_obj[i] for i in indices]
    else:
        fill_palette = palette_obj
    
    # Create figure with proper ranges (excluding NaN values)
    valid_x = x_grid[~np.isnan(x_grid)]
    valid_y = y_grid[~np.isnan(y_grid)]
    
    if len(valid_x) == 0 or len(valid_y) == 0:
        raise ValueError("No valid points after projection transformation")
    
    # Add small padding to ranges
    x_range_pad = (valid_x.max() - valid_x.min()) * 0.02
    y_range_pad = (valid_y.max() - valid_y.min()) * 0.02
    
    p = figure(
        x_range=(valid_x.min() - x_range_pad, valid_x.max() + x_range_pad),
        y_range=(valid_y.min() - y_range_pad, valid_y.max() + y_range_pad),
        width=width, height=height,
        title=title, outline_line_color=None,
        active_scroll='wheel_zoom',
        tools="pan,wheel_zoom,reset,save"  # Explicitly set tools, no default hover
    )
    
    # Add filled contours
    contour_renderer = p.contour(
        x_grid, y_grid, arr,
        levels=level_values,
        fill_color=fill_palette,
    )
    
    
    # Add coastlines using cartopy
    if show_coastlines:
        try:
            coastlines = cfeature.NaturalEarthFeature('physical', 'coastline', '110m')
            
            # Different handling for PlateCarree vs other projections
            if not use_projection or isinstance(projection, ccrs.PlateCarree):
                # For PlateCarree: Simple approach with NaN separation
                x_coords = []
                y_coords = []
                for geom in coastlines.geometries():
                    if isinstance(geom, LineString):
                        coords = np.array(geom.coords)
                        x_coords.extend(coords[:, 0].tolist() + [np.nan])
                        y_coords.extend(coords[:, 1].tolist() + [np.nan])
                    elif isinstance(geom, MultiLineString):
                        for line in geom.geoms:
                            coords = np.array(line.coords)
                            x_coords.extend(coords[:, 0].tolist() + [np.nan])
                            y_coords.extend(coords[:, 1].tolist() + [np.nan])
                
                p.line(x_coords, y_coords, line_color=coastline_color, 
                      line_width=coastline_width)
            else:
                # For other projections: Transform and handle carefully
                def process_line_string(line_string):
                    if isinstance(line_string, (LineString, MultiLineString)):
                        if isinstance(line_string, LineString):
                            lines = [line_string]
                        else:
                            lines = list(line_string.geoms)
                        
                        for line in lines:
                            coords = np.array(line.coords)
                            if len(coords) > 1:
                                # Transform coastline coordinates
                                tt = projection.transform_points(ccrs.PlateCarree(), 
                                                                coords[:, 0], 
                                                                coords[:, 1])
                                x = tt[:, 0]
                                y = tt[:, 1]
                                
                                # Filter invalid points and large jumps
                                valid = ~(np.isnan(x) | np.isnan(y) | np.isinf(x) | np.isinf(y))
                                if np.sum(valid) > 1:
                                    x_valid = x[valid]
                                    y_valid = y[valid]
                                    
                                    # Split on large jumps (discontinuities)
                                    dx = np.diff(x_valid)
                                    dy = np.diff(y_valid)
                                    dist = np.sqrt(dx**2 + dy**2)
                                    threshold = np.nanpercentile(dist, 95) * 3  # Adaptive threshold
                                    
                                    splits = np.where(dist > threshold)[0] + 1
                                    segments = np.split(range(len(x_valid)), splits)
                                    
                                    for seg in segments:
                                        if len(seg) > 1:
                                            p.line(x_valid[seg], y_valid[seg], 
                                                 line_color=coastline_color, 
                                                 line_width=coastline_width)
                
                for geom in coastlines.geometries():
                    process_line_string(geom)
                
        except Exception as e:
            print(f"Warning: Could not load coastlines: {e}")
    
    # Add color bar
    colorbar = contour_renderer.construct_color_bar(title=cbar_title, background_fill_alpha=0)
    p.add_layout(colorbar, 'right')
    
    curdoc().theme = 'dark_minimal'
    p.min_border_right=165;
    p.styles = {'margin-top': '0px','margin-left': '0px','border-radius': '10px','box-shadow': '0 18px 20px rgba(243, 192, 97, 0.2)','padding': '5px','background-color': '#343838','border': '1.5px solid orange'}
    p.min_border_bottom = 20
    p.background_fill_color = '#1f1f1f'
    p.border_fill_color = '#343838'
    p.background_fill_alpha = 0
    p.toolbar.autohide = True
    p.toolbar_location='left'
    p.title.text_font_size = "18pt"
    p.title.text_font = "Courier New"
    p.title.align = "center"

    # Style
    if use_projection:
        p.xaxis.visible = False
        p.yaxis.visible = False
        p.grid.visible = False
    else:
        p.xaxis.axis_label = "Longitude"
        p.yaxis.axis_label = "Latitude"
        p.grid.grid_line_alpha = 0.3

    if sh==1:
        show(p)

    return p

# EXAMPLE !

# import xarray as xr
# import pandas as pd
# import numpy as np

# # Simple coordinates
# lats = np.linspace(-90, 90, 181)
# lons = np.linspace(-180, 180, 360)
# times = pd.date_range('2000-01-01', periods=12, freq='MS')

# # Simple random data
# data = np.random.uniform(50, 300, (len(times), len(lats), len(lons)))

# # Create xarray
# era5_ssr = xr.Dataset(
#     {'ssr': (['time', 'lat', 'lon'], data)},
#     coords={'time': times, 'lat': lats, 'lon': lons}
# )['ssr'].mean('time')

# # Plot with contourf style
# p2 = contourf_map(
#     era5_ssr,
#     title="ERA5 SSR - Mollweide",
#     levels=10,
#     palette='Plasma256',
#     vmin=0,
#     vmax=300, 
#     projection=ccrs.Mollweide(),
#     cbar_title="ERA5 SSR (W/m²)",
# )
