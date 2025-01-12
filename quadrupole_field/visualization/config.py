"""Plot configuration settings."""

from dataclasses import dataclass, field
from typing import Tuple

from matplotlib.colors import LinearSegmentedColormap


def create_electric_colormap() -> LinearSegmentedColormap:
    """Create a blue-white-red colormap for electric potential visualization."""
    return LinearSegmentedColormap.from_list(
        "electric_potential",
        ["#2166AC", "white", "#B2182B"],  # Blue to White to Red
    )


@dataclass
class PlotConfig:
    """Configuration for plot appearance and behavior."""

    # Grid and Resolution
    field_resolution: int = 20  # Number of points in each direction for field grid
    field_extent_factor: float = 1.5  # Factor for field grid extent beyond rod distance
    field_sampling_points: int = 20  # Number of time points to sample for max field
    min_distance_threshold: float = 1e-9  # Minimum distance to avoid singularities
    grid_density: int = 10  # Number of grid lines in each direction

    # Plot Dimensions
    figure_size: tuple[int, int] = (8, 8)  # Width and height of the figure in inches
    plot_limits_factor: float = 1.5  # Plot limits as multiple of rod distance

    # Rod Appearance
    rod_dot_size: int = 100  # Size of the dots representing rods
    rod_zorder: int = 5  # Z-order of rods (higher numbers appear on top)

    # Trajectory Appearance
    trajectory_line_width: int = 1  # Width of the particle trajectory line
    particle_marker_size: int = 8  # Size of the particle marker

    # Field Arrow Appearance
    quiver_alpha: float = 0.6  # Transparency of field arrows
    quiver_scale: int = 15  # Scaling factor for field arrow size
    quiver_width: float = 0.005  # Width of field arrows
    quiver_headwidth: float = 3  # Width of arrow heads relative to shaft
    quiver_headlength: float = 5  # Length of arrow heads
    quiver_headaxislength: float = 4.5  # Length of arrow head base

    # Velocity Arrow Appearance
    velocity_arrow_scale: float = 5.0  # Scaling factor for velocity arrow
    velocity_arrow_width: float = 0.005  # Width of velocity arrow
    velocity_arrow_size: float = 0.2  # Size of velocity arrow relative to plot

    # Animation Settings
    animation_interval: int = 20  # Milliseconds between frames
    animation_fps: int = 30  # Frames per second for saved video
    animation_bitrate: int = 2000  # Bitrate for video encoding
    animation_metadata_artist: str = "Paul Trap Simulation"  # Artist metadata for video

    # Text Display
    velocity_text_x: float = 0.02  # X position of velocity text (figure coordinates)
    velocity_text_y: float = 0.98  # Y position of velocity text (figure coordinates)
    velocity_text_size: int = 10  # Font size for velocity text


@dataclass
class ColorConfig:
    """Configuration for plot colors and color ranges."""

    # Color Maps
    colormap: LinearSegmentedColormap = field(default_factory=create_electric_colormap)
    voltage_range: Tuple[float, float] = (-10, 10)  # Min/max voltage for color scaling

    # Element Colors
    particle_color: str = "black"  # Color of the particle marker
    trajectory_color: str = "black"  # Color of the trajectory line
    velocity_arrow_color: str = "black"  # Color of the velocity arrow
    grid_color: str = "gray"  # Color of the background grid

    # Text Colors
    velocity_text_color: str = "black"  # Color of the velocity text
    velocity_text_box_color: str = "white"  # Color of text background box
    velocity_text_box_alpha: float = 0.7  # Transparency of text background box


# Create instances
PLOT_CONFIG = PlotConfig()
COLOR_CONFIG = ColorConfig()
