"""Electric field visualization component."""

from typing import Any, Tuple

import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import Normalize
from matplotlib.quiver import Quiver
from numpy.typing import NDArray

from quadrupole_field.core.trap import Trap
from quadrupole_field.visualization.config import COLOR_CONFIG, PLOT_CONFIG


class FieldVisualizer:
    """Electric field visualization component."""

    ax: Axes
    trap: Trap
    a: float
    X: NDArray[np.float64]
    Y: NDArray[np.float64]
    Ex: NDArray[np.float64]
    Ey: NDArray[np.float64]
    max_magnitude: float
    quiver: Quiver
    norm: Normalize

    def __init__(
        self, ax: Axes, trap: Trap, a: float, max_field_magnitude: float
    ) -> None:
        self.ax = ax
        self.trap = trap
        self.a = a
        self.max_magnitude = max_field_magnitude
        self.setup_field_grid()
        self.setup_field_plot()

    def setup_field_grid(self) -> None:
        """Set up the grid for electric field visualization."""
        x = np.linspace(
            -self.a * PLOT_CONFIG.field_extent_factor,
            self.a * PLOT_CONFIG.field_extent_factor,
            PLOT_CONFIG.field_resolution,
        )
        y = np.linspace(
            -self.a * PLOT_CONFIG.field_extent_factor,
            self.a * PLOT_CONFIG.field_extent_factor,
            PLOT_CONFIG.field_resolution,
        )
        self.X, self.Y = np.meshgrid(x, y)
        self.Ex = np.zeros_like(self.X)
        self.Ey = np.zeros_like(self.Y)

    def normalize_field(
        self, Ex: NDArray[np.float64], Ey: NDArray[np.float64]
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Normalize the electric field vectors."""
        if self.max_magnitude > 0:
            Ex = Ex / self.max_magnitude
            Ey = Ey / self.max_magnitude
        return Ex, Ey

    def calculate_field_colors(self) -> NDArray[np.float64]:
        """Calculate the electric potential at each point in the field grid."""
        colors = np.zeros_like(self.Ex)
        for i in range(len(self.X)):
            for j in range(len(self.Y)):
                colors[i, j] = sum(
                    rod.electric_potential_at(
                        self.X[i, j], self.Y[i, j], PLOT_CONFIG.min_distance_threshold
                    )
                    for rod in self.trap.rods
                )
        return colors

    def setup_field_plot(self) -> None:
        """Initialize the electric field quiver plot."""
        # Calculate initial field
        for i in range(len(self.X)):
            for j in range(len(self.Y)):
                self.Ex[i, j], self.Ey[i, j] = self.trap.electric_field_at(
                    self.X[i, j], self.Y[i, j]
                )

        # Normalize field vectors using the dedicated method
        Ex_norm, Ey_norm = self.normalize_field(self.Ex, self.Ey)

        # Calculate colors based on potential
        colors = self.calculate_field_colors()
        self.norm = Normalize(vmin=-np.max(np.abs(colors)), vmax=np.max(np.abs(colors)))

        self.quiver = self.ax.quiver(
            self.X,
            self.Y,
            Ex_norm,
            Ey_norm,
            colors.flatten(),
            cmap=COLOR_CONFIG.colormap,
            norm=self.norm,
            alpha=PLOT_CONFIG.quiver_alpha,
            scale=PLOT_CONFIG.quiver_scale,
        )

        # Add colorbar
        self.ax.figure.colorbar(self.quiver, label="Electric Potential")

    def update(self) -> None:
        """Update the electric field visualization."""
        # Calculate current field
        for i in range(len(self.X)):
            for j in range(len(self.Y)):
                self.Ex[i, j], self.Ey[i, j] = self.trap.electric_field_at(
                    self.X[i, j], self.Y[i, j]
                )

        # Normalize field vectors using the dedicated method
        Ex_norm, Ey_norm = self.normalize_field(self.Ex, self.Ey)

        # Update colors
        colors = self.calculate_field_colors()

        # Update quiver
        self.quiver.set_UVC(Ex_norm, Ey_norm, colors.flatten())
