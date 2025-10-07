import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from cartopy.io.img_tiles import GoogleTiles


def create_measurement_map(measurement_points, title="Measurement Map", value_title="Value", 
                          value_unit="", figsize=(8, 8), zoom_level=18, padding_meters=20):
    """
    Create a map visualization with measurement points colored by their values.
    
    Parameters:
    -----------
    measurement_points : list
        List of dictionaries with keys: 'id', 'lat', 'lon', and the value field
    title : str, optional
        Main title for the map (default: "Measurement Map")
    value_title : str, optional
        Title for the value being measured (default: "Value")
    value_unit : str, optional
        Unit for the values (default: "")
    figsize : tuple, optional
        Figure size (width, height) in inches (default: (8, 8))
    zoom_level : int, optional
        Zoom level for the map tiles (default: 18)
    padding_meters : int, optional
        Padding around points in meters (default: 20)
    
    Returns:
    --------
    matplotlib.figure.Figure
        The created figure object
    """
    
    # Create figure and axis
    fig = plt.figure(figsize=figsize)
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Calculate bounds to include all measurement points with padding
    measurement_lats = [point['lat'] for point in measurement_points]
    measurement_lons = [point['lon'] for point in measurement_points]
    
    # Add padding around the points
    padding = padding_meters / 111000  # Convert meters to degrees
    
    min_lat = min(measurement_lats) - padding
    max_lat = max(measurement_lats) + padding
    min_lon = min(measurement_lons) - padding
    max_lon = max(measurement_lons) + padding
    
    # Set extent to include all measurement points
    ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
    
    # Create a custom tile source that focuses on streets
    class StreetOnlyTiles(GoogleTiles):
        def _image_url(self, tile):
            # Use CartoDB Positron tiles which are minimal and street-focused
            x, y, z = tile
            return f"https://tiles.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
    
    street_tiles = StreetOnlyTiles()
    ax.add_image(street_tiles, zoom_level)  # High zoom level for street detail
    
    # Set background to white
    ax.set_facecolor('white')
    
    # Apply grayscale effect to the map tiles
    for image in ax.get_images():
        # Convert to grayscale by averaging RGB channels
        image.set_cmap('gray')
        image.set_clim(0, 1)  # Ensure proper scaling
    
    # Extract values for color mapping (assuming the value field is named after value_title)
    value_field = value_title.lower().replace(' ', '_')
    if value_field not in measurement_points[0]:
        # Try common field names
        for field in ['value', 'latency', 'throughput', 'rtt', 'delay']:
            if field in measurement_points[0]:
                value_field = field
                break
        else:
            raise ValueError(f"Could not find value field in measurement points. Available fields: {list(measurement_points[0].keys())}")
    
    all_values = [point[value_field] for point in measurement_points]
    min_value = min(all_values)
    max_value = max(all_values)
    
    # Plot measurement points as simple circles with color based on values
    for measurement in measurement_points:
        # Normalize value to 0-1 range for color mapping
        normalized_value = (measurement[value_field] - min_value) / (max_value - min_value)
        
        # Use a colormap to get color based on normalized value
        # Red for high values, blue for low values
        color = plt.cm.RdYlBu_r(normalized_value)  # Reverse colormap: red=high, blue=low
        
        # Fixed size for all circles
        size = 60
        
        # Plot measurement point as simple circle without border
        ax.scatter(measurement['lon'], measurement['lat'], s=size, 
                  c=[color], marker='o', alpha=0.8, 
                  transform=ccrs.PlateCarree(), zorder=10)
    
    # Professional title
    ax.set_title(f'{title}\n{value_title} Measurements Along Route', 
                fontsize=18, fontweight='bold', pad=20)
    
    # Create colorbar to show value range
    sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlBu_r, norm=plt.Normalize(vmin=min_value, vmax=max_value))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.8, orientation='horizontal', pad=0.05)
    
    # Create colorbar label
    if value_unit:
        cbar_label = f'{value_title} ({value_unit}) - Red=High, Blue=Low'
    else:
        cbar_label = f'{value_title} - Red=High, Blue=Low'
    
    cbar.set_label(cbar_label, fontsize=12, fontweight='bold')
    cbar.ax.tick_params(labelsize=10)
    
    # Add measurement statistics
    total_measurements = len(measurement_points)
    value_range = f"Range: {min_value:.1f} - {max_value:.1f}"
    if value_unit:
        value_range += f" {value_unit}"
    
    stats_text = f"Total Measurements: {total_measurements}\n{value_range}"
    
    ax.text(0.02, 0.02, stats_text, transform=ax.transAxes, 
           fontsize=10, bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, 
                                 edgecolor='black', linewidth=0.5),
           verticalalignment='bottom')
    
    plt.tight_layout()
    return fig


def save_map(fig, filename, dpi=300):
    """
    Save the map figure to a file.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure to save
    filename : str
        Output filename
    dpi : int, optional
        Resolution in dots per inch (default: 300)
    """
    fig.savefig(filename, dpi=dpi, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"Map saved as '{filename}'!")
