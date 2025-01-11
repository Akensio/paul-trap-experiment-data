"""Configuration settings for simulation and visualization."""

from dataclasses import dataclass, field
from typing import Any

from matplotlib.colors import LinearSegmentedColormap


# Create a function to generate our colormap
def create_electric_colormap() -> LinearSegmentedColormap:
    return LinearSegmentedColormap.from_list(
        "electric_potential",
        [
            "#2166AC",
            "white",
            "#B2182B",
        ],  # Dark blue -> White -> Dark red (matches RdBu_r)
    )


@dataclass
class SimulationConfig:
    dt: float = 0.001  # Smaller timestep for smoother simulation
    total_time: float = 5.0  # Shorter time to focus on stable pattern


@dataclass
class PlotConfig:
    field_resolution: int = 20  # Number of grid points in each direction
    figure_size: tuple[int, int] = (8, 8)  # Figure size in inches
    plot_limits_factor: float = 1.5  # Plot limits as factor of rod distance
    rod_dot_size: int = 100  # Size of rod dots in scatter plot
    rod_zorder: int = 5  # Z-order for rod dots (higher = on top)
    trajectory_line_width: int = 1  # Width of particle trajectory line
    quiver_alpha: float = 0.6  # Transparency of field arrows
    quiver_scale: int = 15  # Scale factor for field arrows
    animation_interval: int = 20  # Animation interval in milliseconds


@dataclass
class ColorConfig:
    colormap: LinearSegmentedColormap = field(
        default_factory=create_electric_colormap
    )  # Our custom colormap
    voltage_range: tuple[float, float] = (
        -10,
        10,
    )  # Voltage range for color normalization
    particle_color: str = "blue"  # Color of the particle dot
    trajectory_color: str = "blue"  # Color of the trajectory line
    grid_color: str = "gray"  # Color of the grid lines


# Create instances
SIMULATION_CONFIG = SimulationConfig()
PLOT_CONFIG = PlotConfig()
COLOR_CONFIG = ColorConfig()
