"""Main visualization coordinator."""
from typing import Any, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
import matplotlib.animation as animation
from quadrupole_field.trap import Trap
from quadrupole_field.plot.field_visualizer import FieldVisualizer
from quadrupole_field.plot.particle_visualizer import ParticleVisualizer
from quadrupole_field.plot.rod_visualizer import RodVisualizer
from quadrupole_field.plot.plot_config import PLOT_CONFIG, COLOR_CONFIG

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
        self.dt = dt
        self.trap = trap  # Store trap reference

        # Setup the plot
        self.fig, self.ax = plt.subplots(figsize=PLOT_CONFIG.figure_size)
        self.ax.set_aspect('equal')
        self.ax.grid(True, color=COLOR_CONFIG.grid_color)
        
        # Set plot limits
        limit = self.a * PLOT_CONFIG.plot_limits_factor
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.set_xlabel('x (m)')
        self.ax.set_ylabel('y (m)')
        
        # Initialize visualizer components
        self.field_vis = FieldVisualizer(self.ax, trap, a)
        self.particle_vis = ParticleVisualizer(self.ax)
        self.rod_vis = RodVisualizer(self.ax, trap)

    def update_frame(self, frame: int) -> List[Any]:
        """Update animation frame."""
        # Update rod voltages first
        voltages = self.voltages_history[frame]
        self.trap.set_voltages(voltages)
        
        # Update field (now with new voltages)
        self.field_vis.update()
        
        # Update particle and trajectory
        self.particle_vis.update(frame, self.positions, self.velocities, self.a)
        
        # Update rod colors
        self.rod_vis.update_colors(voltages)
        
        return []

    def animate(self, save_video: bool = False, filename: str = "animation.mp4") -> None:
        """Create and display the animation."""
        # Create animation
        anim = animation.FuncAnimation(
            self.fig,
            self.update_frame,
            frames=len(self.positions),
            interval=PLOT_CONFIG.animation_interval,
            blit=False
        )

        if save_video:
            writer = animation.FFMpegWriter(
                fps=30,
                metadata=dict(artist="Paul Trap Simulation"),
                bitrate=2000
            )
            anim.save(filename, writer=writer)
            print(f"Video saved as {filename}")

        plt.show()