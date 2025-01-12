"""Electric field visualization component."""

from typing import Any, Tuple

import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import Normalize
from matplotlib.quiver import Quiver
from numpy.typing import NDArray

from quadrupole_field.plot.plot_config import COLOR_CONFIG, PLOT_CONFIG
from quadrupole_field.trap import Trap


class FieldVisualizer:
    def __init__(
        self, ax: Axes, trap: Trap, a: float, voltages_history: NDArray[np.float64]
    ) -> None:
        self.ax = ax
        self.trap = trap
        self.a = a
        self.setup_field_grid()
        self.calculate_max_field(voltages_history)
        self.setup_field_plot()

    def setup_field_grid(self) -> None:
        """Set up the grid for electric field visualization."""
        x = np.linspace(-self.a * 1.5, self.a * 1.5, PLOT_CONFIG.field_resolution)
        y = np.linspace(-self.a * 1.5, self.a * 1.5, PLOT_CONFIG.field_resolution)
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

    def calculate_max_field(self, voltages_history: NDArray[np.float64]) -> None:
        """Calculate maximum field magnitude across all time steps."""
        self.max_magnitude = 0

        # Sample a subset of time points for efficiency
        sample_indices = np.linspace(0, len(voltages_history) - 1, 20, dtype=int)

        for t_idx in sample_indices:
            # Set voltages for this time step
            self.trap.set_voltages(voltages_history[t_idx])

            # Calculate field at each point
            for i in range(len(self.X)):
                for j in range(len(self.Y)):
                    Ex, Ey = self.trap.electric_field_at(self.X[i, j], self.Y[i, j])
                    magnitude = np.sqrt(Ex**2 + Ey**2)
                    if np.isfinite(magnitude):
                        self.max_magnitude = max(self.max_magnitude, magnitude)

    def calculate_field_colors(self) -> NDArray[np.float64]:
        """Calculate colors based on electric potential."""
        colors = np.zeros_like(self.Ex)
        for i in range(len(self.X)):
            for j in range(len(self.Y)):
                potential = 0
                for rod in self.trap.rods:
                    dx = self.X[i, j] - rod.position[0]
                    dy = self.Y[i, j] - rod.position[1]
                    R = np.sqrt(dx**2 + dy**2) + 1e-9
                    potential += rod.voltage / R
                colors[i, j] = potential
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
