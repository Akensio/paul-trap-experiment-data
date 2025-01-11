# main.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from constants import *
from field_calculations import calculate_field_from_electrode
from particle_dynamics import update_particle_position
from visualization import setup_visualization, add_colorbars, update_quiver

# Initialize particle
particle_pos = np.array([0.001, 0, 0])
particle_vel = np.array([0, 0.001, 0])
particle_positions = [particle_pos.copy()]

# Set up visualization
fig, ax, arrow_colormap, pole_colormap, particle_trajectory, particle_marker = setup_visualization()

# Create electrode lines
electrode_lines = []
for electrode_position in electrode_positions:
    z_range = np.linspace(-0.1, 0.1, 100)
    x_coords = np.full_like(z_range, electrode_position[0])
    y_coords = np.full_like(z_range, electrode_position[1])
    (line,) = ax.plot(x_coords, y_coords, z_range, linewidth=3, color="gray")
    electrode_lines.append(line)

# Normalize field magnitudes and electrode charges
field_norm = Normalize(vmin=0, vmax=lambda_amplitude / (2 * np.pi * epsilon_0 * 0.1))
charge_norm = Normalize(vmin=-lambda_amplitude, vmax=lambda_amplitude)

# Add colorbars
add_colorbars(fig, ax, field_norm, arrow_colormap, charge_norm, pole_colormap)

# Placeholder for quiver plot
quiver = None

def update(frame):
    global particle_pos, particle_vel, quiver

    # Current simulation time
    t = frame * dt
    print(f"t is {t}")

    # Dynamic charge densities
    lambda_values = [
        lambda_amplitude * np.sin(omega * t),
        lambda_amplitude * np.sin(omega * t),
        -lambda_amplitude * np.sin(omega * t),
        -lambda_amplitude * np.sin(omega * t),
    ]

    # Update particle dynamics
    particle_pos, particle_vel = update_particle_position(
        particle_pos, particle_vel, electrode_positions, lambda_values
    )
    particle_positions.append(particle_pos.copy())

    # Update particle trajectory
    particle_trajectory.set_data_3d(
        [pos[0] for pos in particle_positions],
        [pos[1] for pos in particle_positions],
        [pos[2] for pos in particle_positions],
    )

    # Update particle marker (current position)
    particle_marker.set_data([particle_pos[0]], [particle_pos[1]])
    particle_marker.set_3d_properties([particle_pos[2]])

    # Update electrode colors dynamically
    for i, electrode_line in enumerate(electrode_lines):
        # Normalize lambda_value: Set a maximum negative value (-lambda_amplitude) to zero, and maximum positive value (lambda_amplitude) to 1
        norm_charge = (lambda_values[i] + lambda_amplitude) / (2 * lambda_amplitude)
        pole_color = pole_colormap(norm_charge)
        electrode_line.set_color(pole_color)

    # Calculate total electric field
    Ex_total, Ey_total, Ez_total = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)
    for i, electrode in enumerate(electrode_positions):
        Ex, Ey, Ez = calculate_field_from_electrode(X, Y, Z, electrode, lambda_values[i])
        Ex_total += Ex
        Ey_total += Ey
        Ez_total += Ez

    # Update the electric field quiver plot
    quiver = update_quiver(ax, X, Y, Z, Ex_total, Ey_total, Ez_total, field_norm, arrow_colormap, quiver)
    ax.set_title(f"Electric Field of Quadrupole (t = {t:.2f} s)")

ani = FuncAnimation(fig, update, frames=20000, interval=50)
plt.show()