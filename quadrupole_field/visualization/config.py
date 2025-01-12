"""Plot configuration settings."""

from dataclasses import dataclass, field
from typing import Tuple

from matplotlib.colors import LinearSegmentedColormap


def create_electric_colormap() -> LinearSegmentedColormap:
    return LinearSegmentedColormap.from_list(
        "electric_potential",
        ["#2166AC", "white", "#B2182B"],
    )


@dataclass
class PlotConfig:
    field_resolution: int = 20
    figure_size: tuple[int, int] = (8, 8)
    plot_limits_factor: float = 1.5
    rod_dot_size: int = 100
    rod_zorder: int = 5
    trajectory_line_width: int = 1
    quiver_alpha: float = 0.6
    quiver_scale: int = 15
    animation_interval: int = 20
    velocity_arrow_scale: float = 5.0
    velocity_arrow_width: float = 0.005
    velocity_arrow_size: float = 0.2


@dataclass
class ColorConfig:
    """Configuration for plot colors."""
    colormap: LinearSegmentedColormap = field(default_factory=create_electric_colormap)
    voltage_range: Tuple[float, float] = (-10, 10)
    particle_color: str = "black"
    trajectory_color: str = "black"
    velocity_arrow_color: str = "black"
    grid_color: str = "gray"


# Create instances
PLOT_CONFIG = PlotConfig()
COLOR_CONFIG = ColorConfig()
