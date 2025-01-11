"""Configuration settings for simulation and visualization."""
from typing import Dict, Any

# Simulation settings
SIMULATION_CONFIG: Dict[str, Any] = {
    "dt": 0.001,                   # Smaller timestep for smoother simulation
    "total_time": 5.0,             # Shorter time to focus on stable pattern
}

# Visualization settings
PLOT_CONFIG: Dict[str, Any] = {
    "field_resolution": 20,        # Number of grid points in each direction
    "figure_size": (8, 8),         # Figure size in inches
    "plot_limits_factor": 1.5,     # Plot limits as factor of rod distance
    "rod_dot_size": 100,          # Size of rod dots in scatter plot
    "rod_zorder": 5,              # Z-order for rod dots (higher = on top)
    "trajectory_line_width": 1,    # Width of particle trajectory line
    "quiver_alpha": 0.6,          # Transparency of field arrows
    "quiver_scale": 15,           # Scale factor for field arrows
    "animation_interval": 20,      # Animation interval in milliseconds
}

# Color settings
COLOR_CONFIG: Dict[str, Any] = {
    "colormap": "RdBu_r",         # Colormap for field and rod visualization
    "voltage_range": (-10, 10),   # Voltage range for color normalization
    "particle_color": "blue",     # Color of the particle dot
    "trajectory_color": "blue",   # Color of the trajectory line
    "grid_color": "gray",        # Color of the grid lines
} 