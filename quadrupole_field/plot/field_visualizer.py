"""Electric field visualization component."""
from typing import Any, Tuple
import numpy as np
from numpy.typing import NDArray
from matplotlib.axes import Axes
from matplotlib.quiver import Quiver
from matplotlib.colors import Normalize
from quadrupole_field.trap import Trap
from quadrupole_field.plot.plot_config import COLOR_CONFIG, PLOT_CONFIG

class FieldVisualizer:
    def __init__(self, ax: Axes, trap: Trap, a: float) -> None:
        self.ax = ax
        self.trap = trap
        self.a = a
        self.setup_field_grid()
        self.calculate_max_field()
        self.setup_field_plot()

    def setup_field_grid(self) -> None:
        """Set up the grid for electric field visualization."""
        x = np.linspace(-self.a * 1.2, self.a * 1.2, PLOT_CONFIG.field_resolution)
        y = np.linspace(-self.a * 1.2, self.a * 1.2, PLOT_CONFIG.field_resolution)
        self.X, self.Y = np.meshgrid(x, y)
        self.Ex = np.zeros_like(self.X)
        self.Ey = np.zeros_like(self.Y)

    def calculate_max_field(self) -> None:
        """Calculate the maximum field strength for normalization."""
        for i in range(self.X.shape[0]):
            for j in range(self.X.shape[1]):
                Ex, Ey = self.trap.electric_field_at(self.X[i, j], self.Y[i, j])
                self.Ex[i, j] = Ex
                self.Ey[i, j] = Ey
        self.max_magnitude = np.sqrt(self.Ex**2 + self.Ey**2).max()

    def calculate_field_colors(self) -> NDArray[np.float64]:
        """Calculate colors based on electric potential."""
        return self.Ex**2 + self.Ey**2

    def setup_field_plot(self) -> None:
        """Initialize the electric field quiver plot."""
        # Create quiver with initial colors
        colors = self.calculate_field_colors()
        norm = Normalize(vmin=-np.max(np.abs(colors)), vmax=np.max(np.abs(colors)))

        self.quiver = self.ax.quiver(
            self.X,
            self.Y,
            self.Ex,
            self.Ey,
            colors.flatten(),
            cmap=COLOR_CONFIG.colormap,
            norm=norm,
            alpha=PLOT_CONFIG.quiver_alpha,
            scale=PLOT_CONFIG.quiver_scale,
        )

        # Add colorbar
        self.ax.figure.colorbar(self.quiver, label="Electric Field Strength")

    def update(self) -> None:
        """Update the electric field visualization."""
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