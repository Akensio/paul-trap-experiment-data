"""Particle trajectory visualization component."""
from typing import Any
import numpy as np
from numpy.typing import NDArray
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from quadrupole_field.plot.plot_config import COLOR_CONFIG, PLOT_CONFIG

class ParticleVisualizer:
    def __init__(self, ax: Axes) -> None:
        self.ax = ax
        self.setup_particle_plots()
        
    def setup_particle_plots(self) -> None:
        """Initialize particle and trajectory plots."""
        self.particle_dot, = self.ax.plot(
            [], [], "o",
            color=COLOR_CONFIG.particle_color,
            label="Particle",
            markersize=8
        )
        self.trajectory_line, = self.ax.plot(
            [], [], "-",
            color=COLOR_CONFIG.trajectory_color,
            lw=PLOT_CONFIG.trajectory_line_width,
            label="Trajectory"
        )
        self.velocity_arrow = self.ax.quiver(
            [], [], [], [],
            color=COLOR_CONFIG.velocity_arrow_color,
            scale=PLOT_CONFIG.velocity_arrow_scale,
            width=PLOT_CONFIG.velocity_arrow_width,
            label='Velocity Vector'
        )
        self.velocity_text = self.ax.text(
            0.02, 0.98, '',
            transform=self.ax.transAxes,
            verticalalignment='top',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')
        )

    def update(self, frame: int, positions: NDArray[np.float64], velocities: NDArray[np.float64], a: float) -> None:
        """Update particle visualization for the current frame."""
        if frame == 0:
            self.particle_dot.set_data([positions[0, 0]], [positions[0, 1]])
            self.trajectory_line.set_data([], [])
            return

        x_traj, y_traj = positions[:frame, 0], positions[:frame, 1]
        current_pos = positions[frame]
        current_vel = velocities[frame]
        
        self.particle_dot.set_data([current_pos[0]], [current_pos[1]])
        self.trajectory_line.set_data(x_traj, y_traj)
        
        # Update velocity vector and text
        velocity = np.linalg.norm(current_vel)
        self.velocity_text.set_text(f'Speed: {velocity:.2f} m/s')
        
        if velocity > 0:
            normalized_vel = current_vel / velocity * PLOT_CONFIG.velocity_arrow_size * a
            self.velocity_arrow.set_offsets([current_pos[0], current_pos[1]])
            self.velocity_arrow.set_UVC(normalized_vel[0], normalized_vel[1])