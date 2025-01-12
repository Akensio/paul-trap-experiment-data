"""Rod visualization component."""

from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import Normalize
from numpy.typing import NDArray

from quadrupole_field.plot.plot_config import COLOR_CONFIG, PLOT_CONFIG
from quadrupole_field.trap import Trap


class RodVisualizer:
    def __init__(self, ax: Axes, trap: Trap) -> None:
        self.ax = ax
        self.trap = trap
        self.setup_rods()

    def setup_rods(self) -> None:
        """Initialize rod visualization."""
        rod_positions = np.array([rod.position for rod in self.trap.rods])
        self.rod_dots = self.ax.scatter(
            rod_positions[:, 0],
            rod_positions[:, 1],
            c=[0, 0, 0, 0],  # Initial colors
            cmap=COLOR_CONFIG.colormap,
            norm=Normalize(
                vmin=COLOR_CONFIG.voltage_range[0], vmax=COLOR_CONFIG.voltage_range[1]
            ),
            s=PLOT_CONFIG.rod_dot_size,
            zorder=PLOT_CONFIG.rod_zorder,
        )

    def update_colors(self, voltages: NDArray[np.float64]) -> None:
        """Update rod colors based on voltages."""
        self.rod_dots.set_array(voltages)
