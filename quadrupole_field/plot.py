import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from numpy.typing import NDArray
from trap import Trap
from typing import Tuple, Any


class PaulTrapVisualizer:
    def __init__(
        self,
        positions: NDArray[np.float64],
        voltages_history: NDArray[np.float64],
        a: float,
        trap: Trap,
        dt: float,
        field_resolution: int = 20,
    ) -> None:
        """Initialize the visualizer with simulation data."""
        self.positions = positions
        self.voltages_history = voltages_history
        self.a = a
        self.trap = trap
        self.dt = dt
        self.field_resolution = field_resolution
        
        # Setup the plot
        self.setup_plot()
        self.setup_field_grid()
        self.calculate_max_field()
        
    def setup_plot(self) -> None:
        """Initialize the matplotlib figure and axes."""
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_xlim(-1.5 * self.a, 1.5 * self.a)
        self.ax.set_ylim(-1.5 * self.a, 1.5 * self.a)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title("Particle Trajectory in Paul Trap (Animation with Field)")
        self.ax.grid()

        # Plot the rods
        self.ax.plot([self.a, -self.a, 0, 0], [0, 0, self.a, -self.a], "ro", label="Rods")
        self.ax.legend()

        # Initialize particle and trajectory plots
        (self.particle_dot,) = self.ax.plot([], [], "bo", label="Particle")
        (self.trajectory_line,) = self.ax.plot([], [], "b-", lw=1, label="Trajectory")

    def setup_field_grid(self) -> None:
        """Setup the grid for the electric field quiver plot."""
        x = np.linspace(-1.5 * self.a, 1.5 * self.a, self.field_resolution)
        y = np.linspace(-1.5 * self.a, 1.5 * self.a, self.field_resolution)
        self.X, self.Y = np.meshgrid(x, y)
        self.Ex = np.zeros_like(self.X)
        self.Ey = np.zeros_like(self.Y)
        
    def calculate_max_field(self) -> None:
        """Calculate maximum field magnitude across all time steps."""
        self.max_magnitude = 0
        for voltages in self.voltages_history:
            self.trap.set_voltages(voltages)
            for i in range(len(self.X)):
                for j in range(len(self.Y)):
                    self.Ex[i, j], self.Ey[i, j] = self.trap.electric_field_at(
                        self.X[i, j], self.Y[i, j]
                    )
            magnitudes = np.sqrt(self.Ex**2 + self.Ey**2)
            self.max_magnitude = max(
                self.max_magnitude, np.max(magnitudes[np.isfinite(magnitudes)])
            )

    def normalize_field(
        self, Ex: NDArray[np.float64], Ey: NDArray[np.float64]
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Normalize the electric field vectors."""
        if self.max_magnitude > 0:
            Ex = Ex / self.max_magnitude
            Ey = Ey / self.max_magnitude
        return Ex, Ey

    def init_animation(self) -> tuple[Any, ...]:
        """Initialize the animation."""
        self.particle_dot.set_data([], [])
        self.trajectory_line.set_data([], [])
        self.quiver.set_UVC(self.Ex, self.Ey)
        return self.particle_dot, self.trajectory_line, self.quiver

    def update_frame(self, frame: int) -> tuple[Any, ...]:
        """Update function for each animation frame."""
        if frame == 0:
            return self.handle_first_frame()
        return self.handle_normal_frame(frame)

    def handle_first_frame(self) -> tuple[Any, ...]:
        """Handle the first frame of the animation."""
        self.particle_dot.set_data([self.positions[0, 0]], [self.positions[0, 1]])
        self.trajectory_line.set_data([], [])
        self.update_field()
        return self.particle_dot, self.trajectory_line, self.quiver

    def handle_normal_frame(self, frame: int) -> tuple[Any, ...]:
        """Handle a normal frame of the animation."""
        self.current_frame = frame  # Update current frame
        x_traj, y_traj = self.positions[:frame, 0], self.positions[:frame, 1]
        self.particle_dot.set_data([x_traj[-1]], [y_traj[-1]])
        self.trajectory_line.set_data(x_traj, y_traj)
        
        self.trap.set_voltages(self.voltages_history[frame])
        self.update_field()
        return self.particle_dot, self.trajectory_line, self.quiver

    def calculate_field_colors(self) -> NDArray[np.float64]:
        """Calculate colors based on the electric potential."""
        colors = np.zeros_like(self.Ex)
        for i in range(len(self.X)):
            for j in range(len(self.Y)):
                # Sum up contributions from all rods
                potential = 0
                for rod, voltage in zip(self.trap.rods, self.voltages_history[self.current_frame]):
                    dx = self.X[i, j] - rod.position[0]
                    dy = self.Y[i, j] - rod.position[1]
                    R = np.sqrt(dx**2 + dy**2) + 1e-9
                    potential += voltage / R
                colors[i, j] = potential
        return colors

    def update_field(self) -> None:
        """Update and normalize the electric field."""
        for i in range(len(self.X)):
            for j in range(len(self.Y)):
                self.Ex[i, j], self.Ey[i, j] = self.trap.electric_field_at(
                    self.X[i, j], self.Y[i, j]
                )
        Ex_norm, Ey_norm = self.normalize_field(self.Ex, self.Ey)
        
        # Calculate colors based on potential
        colors = self.calculate_field_colors()
        norm = Normalize(vmin=-np.max(np.abs(colors)), vmax=np.max(np.abs(colors)))
        
        # Update quiver with colors
        self.quiver.set_UVC(Ex_norm, Ey_norm)
        self.quiver.set_array(colors.flatten())

    def animate(self) -> None:
        """Create and display the animation."""
        self.current_frame = 0  # Add frame tracking
        
        # Create quiver with initial colors
        colors = self.calculate_field_colors()
        norm = Normalize(vmin=-np.max(np.abs(colors)), vmax=np.max(np.abs(colors)))
        
        self.quiver = self.ax.quiver(
            self.X, self.Y, self.Ex, self.Ey,
            colors.flatten(),
            cmap='RdBu_r',  # Red-White-Blue colormap (reversed)
            norm=norm,
            alpha=0.6,
            scale=15
        )
        
        # Add colorbar
        plt.colorbar(self.quiver, label='Electric Potential')
        
        self.anim = FuncAnimation(
            self.fig,
            self.update_frame,
            frames=len(self.positions),
            init_func=self.init_animation,
            blit=True,
            interval=20,
        )
        plt.show()
