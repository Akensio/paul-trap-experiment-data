"""Electric field visualization component."""
from typing import Any, Tuple
import numpy as np
from numpy.typing import NDArray
from matplotlib.axes import Axes
from matplotlib.quiver import Quiver
from ..trap import Trap
from .plot_config import PLOT_CONFIG

class FieldVisualizer:
    def __init__(self, ax: Axes, trap: Trap, a: float) -> None:
        self.ax = ax
        self.trap = trap
        self.a = a
        self.field_resolution = PLOT_CONFIG.field_resolution
        self.setup_field_grid()
        self.calculate_max_field()
        
    def setup_field_grid(self) -> None:
        """Setup the grid for the electric field quiver plot."""
        x = np.linspace(-1.5 * self.a, 1.5 * self.a, self.field_resolution)
        y = np.linspace(-1.5 * self.a, 1.5 * self.a, self.field_resolution)
        self.X, self.Y = np.meshgrid(x, y)
        self.Ex = np.zeros_like(self.X)
        self.Ey = np.zeros_like(self.Y)
        self.quiver = self.ax.quiver(
            self.X, self.Y, self.Ex, self.Ey,
            alpha=PLOT_CONFIG.quiver_alpha,
            scale=PLOT_CONFIG.quiver_scale,
        )

    def calculate_max_field(self) -> None:
        """Calculate maximum field magnitude across all time steps."""
        self.max_magnitude = 0
        for i in range(len(self.X)):
            for j in range(len(self.Y)):
                self.Ex[i, j], self.Ey[i, j] = self.trap.electric_field_at(
                    self.X[i, j], self.Y[i, j]
                )
        magnitudes = np.sqrt(self.Ex**2 + self.Ey**2)
        self.max_magnitude = np.max(magnitudes[np.isfinite(magnitudes)])

    def update_field(self) -> None:
        """Update the electric field visualization."""
        for i in range(len(self.X)):
            for j in range(len(self.Y)):
                self.Ex[i, j], self.Ey[i, j] = self.trap.electric_field_at(
                    self.X[i, j], self.Y[i, j]
                )
        Ex_norm, Ey_norm = self.normalize_field(self.Ex, self.Ey)
        self.quiver.set_UVC(Ex_norm, Ey_norm)

    def normalize_field(
        self, Ex: NDArray[np.float64], Ey: NDArray[np.float64]
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Normalize the electric field vectors."""
        if self.max_magnitude > 0:
            Ex = Ex / self.max_magnitude
            Ey = Ey / self.max_magnitude
        return Ex, Ey 