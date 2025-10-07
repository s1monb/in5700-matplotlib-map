import matplotlib.pyplot as plt
from map_visualizer import create_measurement_map, save_map

# Example measurement data
measurement_points = [
    # Central Station area
    {'id': 'Point_01', 'lat': 59.9115, 'lon': 10.7522, 'latency': 12.5, 'timestamp': '2024-01-15 14:30:00'},
    {'id': 'Point_02', 'lat': 59.9118, 'lon': 10.7520, 'latency': 15.2, 'timestamp': '2024-01-15 14:30:15'},
    {'id': 'Point_03', 'lat': 59.9121, 'lon': 10.7518, 'latency': 8.7, 'timestamp': '2024-01-15 14:30:30'},
    {'id': 'Point_04', 'lat': 59.9124, 'lon': 10.7516, 'latency': 22.1, 'timestamp': '2024-01-15 14:30:45'},
    {'id': 'Point_05', 'lat': 59.9127, 'lon': 10.7514, 'latency': 18.9, 'timestamp': '2024-01-15 14:31:00'},
    
    # Towards Aker Brygge
    {'id': 'Point_21', 'lat': 59.9165, 'lon': 10.7470, 'latency': 18.3, 'timestamp': '2024-01-15 14:35:00'}
]

if __name__ == "__main__":
    # Create driving route map with custom parameters
    print("Creating driving route measurement map...")
    
    fig = create_measurement_map(
        measurement_points=measurement_points,
        title="Oslo City - Latency",
        value_title="Latency",
        value_unit="ms",
        figsize=(8, 8),
        zoom_level=18,
        padding_meters=20
    )
    
    # Save the map
    save_map(fig, 'oslo_driving_route_measurements.png', dpi=300)
    plt.show()