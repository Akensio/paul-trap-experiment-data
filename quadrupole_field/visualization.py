# visualization.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize, LinearSegmentedColormap
from constants import lambda_amplitude, omega, epsilon_0, electrodes, X, Y, Z, dt
from field_calculations import calculate_field_from_electrode
from particle_dynamics import update_particle_position

def setup_visualization():
    """
    Sets up the 3D visualization for the quadrupole field simulation.
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Create color maps for arrows and poles
    arrow_colors = [(0, "gray"), (0.5, "cyan"), (1, "blue")]
    arrow_colormap = LinearSegmentedColormap.from_list("arrow_colormap", arrow_colors)

    pole_colors = [(0, "red"), (1, "blue")]
    pole_colormap = LinearSegmentedColormap.from_list("pole_colormap", pole_colors)

    # Initialize the particle trajectory and marker
    particle_trajectory, = ax.plot(
        [], [], [], color="black", linewidth=2, label="Particle Trajectory"
    )
    particle_marker, = ax.plot([], [], [], "o", color="black", markersize=5, label="Particle")

    # Set axis limits for visualization
    ax.set_xlim([-0.15, 0.15])
    ax.set_ylim([-0.15, 0.15])
    ax.set_zlim([-0.15, 0.15])
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.legend()

    # Return visualization objects
    return fig, ax, arrow_colormap, pole_colormap, particle_trajectory, particle_marker

def update_animation(
    frame, particle_pos, particle_vel, particle_positions,
    electrode_lines, quiver, field_norm, ax, particle_trajectory,
    particle_marker, arrow_colormap, pole_colormap
):
    """
    Updates the animation for each frame.

    Args:
        frame: Current frame number.
        particle_pos: Current particle position as a numpy array.
        particle_vel: Current particle velocity as a numpy array.
        particle_positions: List of all particle positions for trajectory visualization.
        electrode_lines: List of electrode line plot objects.
        quiver: The quiver plot object for electric field visualization.
        field_norm: Normalization for the field magnitudes.
        ax: The 3D axes object.
        particle_trajectory: The line object representing the particle's trajectory.
        particle_marker: The marker object representing the particle's current position.
        arrow_colormap: Colormap for the field arrows.
        pole_colormap: Colormap for the electrode poles.
    """
    t = frame * dt  # Time for the current frame
    lambda_values = [
        lambda_amplitude * np.sin(omega * t),
        lambda_amplitude * np.sin(omega * t),
        -lambda_amplitude * np.sin(omega * t),
        -lambda_amplitude * np.sin(omega * t),
    ]

    # Update particle dynamics
    particle_pos, particle_vel = update_particle_position(
        particle_pos, particle_vel, electrodes, lambda_values
    )
    particle_positions.append(particle_pos.copy())

    # Update particle trajectory
    particle_trajectory.set_data_3d(
        [pos[0] for pos in particle_positions],
        [pos[1] for pos in particle_positions],
        [pos[2] for pos in particle_positions],
    )

    # Update particle marker
    particle_marker.set_data([particle_pos[0]], [particle_pos[1]])  # x and y
    particle_marker.set_3d_properties([particle_pos[2]])  # z

    # Update electrode colors
    for i, electrode_line in enumerate(electrode_lines):
        norm_charge = (lambda_values[i] + lambda_amplitude) / (2 * lambda_amplitude)
        pole_color = pole_colormap(norm_charge)
        electrode_line.set_color(pole_color)

    # Calculate electric field
    Ex_total, Ey_total, Ez_total = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)
    for i, electrode in enumerate(electrodes):
        Ex, Ey, Ez = calculate_field_from_electrode(X, Y, Z, electrode, lambda_values[i])
        Ex_total += Ex
        Ey_total += Ey
        Ez_total += Ez

    # Compute field magnitudes and normalize
    field_magnitude = np.sqrt(Ex_total**2 + Ey_total**2 + Ez_total**2)
    field_magnitude_normalized = field_norm(field_magnitude)
    colors = arrow_colormap(field_magnitude_normalized.ravel())

    # Update the electric field quiver plot
    if quiver:
        quiver.remove()
    quiver = ax.quiver(
        X, Y, Z,
        Ex_total, Ey_total, Ez_total,
        length=0.01, colors=colors, alpha=0.8, normalize=True
    )

    # Update the title
    ax.set_title(f"Electric Field of Quadrupole (t = {t:.2f} s)")

    return particle_pos, particle_vel, quiver