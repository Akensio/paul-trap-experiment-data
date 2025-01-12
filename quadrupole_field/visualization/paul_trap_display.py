"""Main visualization coordinator for the Paul trap simulation."""

from typing import Any, List

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
from numpy.typing import NDArray

from quadrupole_field.core.trap import Trap
from quadrupole_field.utils.field_analysis import calculate_max_field_magnitude
from quadrupole_field.visualization.components.field import FieldVisualizer
from quadrupole_field.visualization.components.particle import ParticleVisualizer
from quadrupole_field.visualization.components.rod import RodVisualizer
from quadrupole_field.visualization.config import COLOR_CONFIG, PLOT_CONFIG


class PaulTrapVisualizer:
    """Main visualization coordinator for the Paul trap simulation."""

    # Data arrays
    positions: NDArray[np.float64]
    velocities: NDArray[np.float64]
    voltages_history: NDArray[np.float64]

    # Physical parameters
    a: float
    dt: float
    trap: Trap

    # Matplotlib objects
    fig: Figure
    ax: Axes

    # Visualization components
    field_vis: FieldVisualizer
    particle_vis: ParticleVisualizer
    rod_vis: RodVisualizer

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

        self.setup_figure()
        self.setup_visualizers()

    def setup_figure(self) -> None:
        """Setup the plot."""
        self.fig, self.ax = plt.subplots(figsize=PLOT_CONFIG.figure_size)
        self.ax.set_aspect("equal")
        self.ax.grid(True, color=COLOR_CONFIG.grid_color)

        # Set plot limits
        limit = self.a * PLOT_CONFIG.plot_limits_factor
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.set_xlabel("x (m)")
        self.ax.set_ylabel("y (m)")

    def setup_visualizers(self) -> None:
        """Setup the visualization components."""
        # Calculate maximum field magnitude for normalization
        max_field = calculate_max_field_magnitude(
            self.trap, self.voltages_history, self.a
        )

        # Initialize visualization components
        self.field_vis = FieldVisualizer(
            self.ax, self.trap, self.a, max_field
        )
        self.particle_vis = ParticleVisualizer(self.ax)
        self.rod_vis = RodVisualizer(self.ax, self.trap)

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

    def animate(
        self, save_video: bool = False, filename: str = "animation.mp4"
    ) -> None:
        """Create and display the animation."""
        # Create animation
        anim = FuncAnimation(
            self.fig,
            self.update_frame,
            frames=len(self.positions),
            interval=PLOT_CONFIG.animation_interval,
            blit=False,
        )

        if save_video:
            writer = FFMpegWriter(
                fps=PLOT_CONFIG.animation_fps,
                metadata=dict(artist=PLOT_CONFIG.animation_metadata_artist),
                bitrate=PLOT_CONFIG.animation_bitrate,
            )
            anim.save(filename, writer=writer)
            print(f"Video saved as {filename}")

        plt.show()
