# main.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from constants import *
from field_calculations import calculate_field_from_electrode
from particle_dynamics import update_particle_position
from visualization import setup_visualization

# Initialize particle
particle_pos = np.array([0.05, 0, 0])  # Starting position
particle_vel = np.array([0, 0.01, 0])  # Starting velocity
particle_positions = [particle_pos.copy()]  # List to store trajectory

# Set up visualization
fig, ax, arrow_colormap, pole_colormap, particle_trajectory, particle_marker = setup_visualization()

# Create electrode lines
electrode_lines = []
for electrode in electrodes:
    pos = electrode["position"]
    z_range = np.linspace(-0.1, 0.1, 100)  # Line range for electrodes
    x_coords = np.full_like(z_range, pos[0])
    y_coords = np.full_like(z_range, pos[1])
    (line,) = ax.plot(
        x_coords, y_coords, z_range, linewidth=3, color="gray"  # Neutral color initially
    )
    electrode_lines.append(line)

# Normalize field magnitudes
field_norm = Normalize(vmin=0, vmax=lambda_amplitude / (2 * np.pi * epsilon_0 * 0.1))

# Placeholder for quiver plot (electric field visualization)
quiver = None

# Update function for the animation
def update(
    frame
):
    """
    Updates the animation for each frame.

    Args:
        frame: Current frame number.

    Returns:
        Updated particle position, velocity, and quiver plot.
    """
    global particle_pos, particle_vel, quiver

    # Current simulation time
    t = frame * dt

    # Dynamic charge densities
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
        [pos[0] for pos in particle_positions],  # x-coordinates
        [pos[1] for pos in particle_positions],  # y-coordinates
        [pos[2] for pos in particle_positions],  # z-coordinates
    )

    # Update particle marker (current position)
    particle_marker.set_data([particle_pos[0]], [particle_pos[1]])  # x and y as lists
    particle_marker.set_3d_properties([particle_pos[2]])  # z as a list

    # Update electrode colors dynamically
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

    # Update the plot title with the current time
    ax.set_title(f"Electric Field of Quadrupole (t = {t:.2f} s)")

    return particle_pos, particle_vel, quiver


# Create the animation
ani = FuncAnimation(
    fig,
    update,
    frames=100,
    interval=50,
)

# Show the plot
plt.show()