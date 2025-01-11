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
        self.setup_field_plot()

    def setup_field_grid(self) -> None:
        """Set up the grid for electric field visualization."""
        x = np.linspace(-self.a * 1.2, self.a * 1.2, PLOT_CONFIG.field_resolution)
        y = np.linspace(-self.a * 1.2, self.a * 1.2, PLOT_CONFIG.field_resolution)
        self.X, self.Y = np.meshgrid(x, y)

    def calculate_field(self) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Calculate the current electric field."""
        Ex = np.zeros_like(self.X)
        Ey = np.zeros_like(self.Y)
        
        for i in range(self.X.shape[0]):
            for j in range(self.X.shape[1]):
                Ex[i, j], Ey[i, j] = self.trap.electric_field_at(
                    self.X[i, j], self.Y[i, j]
                )
        
        return Ex, Ey

    def calculate_field_colors(self, Ex: NDArray[np.float64], Ey: NDArray[np.float64]) -> NDArray[np.float64]:
        """Calculate colors based on electric potential."""
        return Ex**2 + Ey**2

    def setup_field_plot(self) -> None:
        """Initialize the electric field quiver plot."""
        # Calculate initial field
        Ex, Ey = self.calculate_field()
        colors = self.calculate_field_colors(Ex, Ey)
        
        # Set up normalization
        self.norm = Normalize(vmin=0, vmax=np.max(np.abs(colors)))

        self.quiver = self.ax.quiver(
            self.X,
            self.Y,
            Ex,
            Ey,
            colors.flatten(),
            cmap=COLOR_CONFIG.colormap,
            norm=self.norm,
            alpha=PLOT_CONFIG.quiver_alpha,
            scale=PLOT_CONFIG.quiver_scale,
        )

        # Add colorbar
        self.ax.figure.colorbar(self.quiver, label="Electric Field Strength")

    def update(self) -> None:
        """Update the electric field visualization."""
        Ex, Ey = self.calculate_field()
        colors = self.calculate_field_colors(Ex, Ey)
        
        self.quiver.set_UVC(Ex, Ey, colors.flatten()) 