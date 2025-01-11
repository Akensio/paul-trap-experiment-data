from typing import Any, Tuple

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from config import COLOR_CONFIG, PLOT_CONFIG
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from numpy.typing import NDArray
from trap import Trap


class PaulTrapVisualizer:
    def __init__(
        self,
        positions: NDArray[np.float64],
        velocities: NDArray[np.float64],
        voltages_history: NDArray[np.float64],
        a: float,
        trap: Trap,
        dt: float,
    ) -> None:
        """Initialize the visualizer with simulation data."""
        self.positions = positions
        self.velocities = velocities
        self.voltages_history = voltages_history
        self.a = a
        self.trap = trap
        self.dt = dt
        self.field_resolution = PLOT_CONFIG.field_resolution

        # Setup the plot
        self.setup_plot()
        self.setup_field_grid()
        self.calculate_max_field()

        # Add velocity text
        self.velocity_text = self.ax.text(
            0.02, 0.98, '',  # Position in axes coordinates
            transform=self.ax.transAxes,  # Use axes coordinates
            verticalalignment='top',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')
        )

    def setup_plot(self) -> None:
        """Initialize the matplotlib figure and axes."""
        self.fig, self.ax = plt.subplots(figsize=PLOT_CONFIG.figure_size)
        limit = self.a * PLOT_CONFIG.plot_limits_factor
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title("Particle Trajectory in Paul Trap (Animation with Field)")
        self.ax.grid()

        # Plot the rods with initial colors
        rod_positions = np.array([rod.position for rod in self.trap.rods])
        self.rod_dots = self.ax.scatter(
            rod_positions[:, 0],
            rod_positions[:, 1],
            c=self.voltages_history[0],
            cmap=COLOR_CONFIG.colormap,
            norm=Normalize(
                vmin=COLOR_CONFIG.voltage_range[0], vmax=COLOR_CONFIG.voltage_range[1]
            ),
            s=PLOT_CONFIG.rod_dot_size,
            zorder=PLOT_CONFIG.rod_zorder,
        )

        # Initialize particle and trajectory plots
        (self.particle_dot,) = self.ax.plot(
            [], [], "o", color=COLOR_CONFIG.particle_color, label="Particle"
        )
        (self.trajectory_line,) = self.ax.plot(
            [],
            [],
            "-",
            color=COLOR_CONFIG.trajectory_color,
            lw=PLOT_CONFIG.trajectory_line_width,
            label="Trajectory",
        )
        self.ax.grid(color=COLOR_CONFIG.grid_color)

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
        self.velocity_text.set_text('')
        return self.particle_dot, self.trajectory_line, self.quiver, self.velocity_text

    def update_frame(self, frame: int) -> tuple[Any, ...]:
        """Update function for each animation frame."""
        if frame == 0:
            return self.handle_first_frame()
        
        # Update velocity display using stored velocity
        velocity = np.linalg.norm(self.velocities[frame])
        self.velocity_text.set_text(f'Velocity: {velocity:.2f} m/s')
        
        self.current_frame = frame
        x_traj, y_traj = self.positions[:frame, 0], self.positions[:frame, 1]
        self.particle_dot.set_data([x_traj[-1]], [y_traj[-1]])
        self.trajectory_line.set_data(x_traj, y_traj)

        self.trap.set_voltages(self.voltages_history[frame])
        self.update_field()
        self.update_rod_colors(frame)
        
        return self.particle_dot, self.trajectory_line, self.quiver, self.rod_dots, self.velocity_text

    def handle_first_frame(self) -> tuple[Any, ...]:
        """Handle the first frame of the animation."""
        self.particle_dot.set_data([self.positions[0, 0]], [self.positions[0, 1]])
        self.trajectory_line.set_data([], [])
        self.update_field()
        return self.particle_dot, self.trajectory_line, self.quiver, self.velocity_text

    def handle_normal_frame(self, frame: int) -> tuple[Any, ...]:
        """Handle a normal frame of the animation."""
        self.current_frame = frame
        x_traj, y_traj = self.positions[:frame, 0], self.positions[:frame, 1]
        self.particle_dot.set_data([x_traj[-1]], [y_traj[-1]])
        self.trajectory_line.set_data(x_traj, y_traj)

        self.trap.set_voltages(self.voltages_history[frame])
        self.update_field()
        self.update_rod_colors(frame)
        return self.particle_dot, self.trajectory_line, self.quiver, self.rod_dots, self.velocity_text

    def calculate_field_colors(self) -> NDArray[np.float64]:
        """Calculate colors based on the electric potential."""
        colors = np.zeros_like(self.Ex)
        for i in range(len(self.X)):
            for j in range(len(self.Y)):
                # Sum up contributions from all rods
                potential = 0
                for rod, voltage in zip(
                    self.trap.rods, self.voltages_history[self.current_frame]
                ):
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

    def animate(
        self, save_video: bool = False, filename: str = "paul_trap.mp4"
    ) -> None:
        """Create and display the animation, optionally saving to video."""
        self.current_frame = 0

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
        plt.colorbar(self.quiver, label="Electric Potential")

        self.anim = FuncAnimation(
            self.fig,
            self.update_frame,
            frames=len(self.positions),
            init_func=self.init_animation,
            blit=True,
            interval=PLOT_CONFIG.animation_interval,
        )

        if save_video:
            # Set up the writer
            writer = animation.FFMpegWriter(
                fps=30, metadata=dict(artist="Paul Trap Simulation"), bitrate=2000
            )

            # Save the animation
            self.anim.save(filename, writer=writer)
            print(f"Video saved as {filename}")

        plt.show()

    def update_rod_colors(self, frame: int) -> None:
        """Update the rod colors based on their current voltages."""
        self.rod_dots.set_array(np.array(self.voltages_history[frame]))
