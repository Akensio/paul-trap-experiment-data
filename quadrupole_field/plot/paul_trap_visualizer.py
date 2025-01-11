"""Main visualization coordinator."""
from typing import Any, Tuple
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from matplotlib.animation import FuncAnimation
from ..trap import Trap
from .field_visualizer import FieldVisualizer
from .particle_visualizer import ParticleVisualizer
from .rod_visualizer import RodVisualizer
from .plot_config import PLOT_CONFIG

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
        self.positions = positions
        self.velocities = velocities
        self.voltages_history = voltages_history
        self.a = a
        self.trap = trap
        self.dt = dt

        # Setup main figure
        self.fig, self.ax = plt.subplots(figsize=PLOT_CONFIG.figure_size)
        self.setup_axes()

        # Initialize components
        self.field_viz = FieldVisualizer(self.ax, trap, a)
        self.particle_viz = ParticleVisualizer(self.ax)
        self.rod_viz = RodVisualizer(self.ax, trap)

    def setup_axes(self) -> None:
        """Setup the plot axes."""
        limit = self.a * PLOT_CONFIG.plot_limits_factor
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title("Particle Trajectory in Paul Trap")
        self.ax.grid(color=COLOR_CONFIG.grid_color)

    def update_frame(self, frame: int) -> tuple[Any, ...]:
        """Update all visualization components."""
        self.trap.set_voltages(self.voltages_history[frame])
        
        self.field_viz.update_field()
        self.particle_viz.update(frame, self.positions, self.velocities, self.a)
        self.rod_viz.update_colors(self.voltages_history[frame])
        
        return (self.particle_viz.particle_dot, self.particle_viz.trajectory_line,
                self.field_viz.quiver, self.particle_viz.velocity_text,
                self.particle_viz.velocity_arrow, self.rod_viz.rod_dots)

    def animate(self, save_video: bool = False, filename: str = "") -> None:
        """Create and display the animation."""
        anim = FuncAnimation(
            self.fig, self.update_frame,
            frames=len(self.positions),
            interval=PLOT_CONFIG.animation_interval,
            blit=True
        )
        if save_video:
            anim.save(filename)
        plt.show()