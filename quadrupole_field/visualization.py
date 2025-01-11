# visualization.py

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.cm import ScalarMappable

def setup_visualization():
    """
    Sets up the 3D visualization for the simulation, including color maps, axis limits,
    particle trajectory, quiver plot placeholders, and colorbars.
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Create color maps
    arrow_colors = [(0, "gray"), (0.5, "cyan"), (1, "blue")]
    arrow_colormap = LinearSegmentedColormap.from_list("arrow_colormap", arrow_colors)

    pole_colors = [(0, "red"), (1, "blue")]
    pole_colormap = LinearSegmentedColormap.from_list("pole_colormap", pole_colors)

    # Initialize particle trajectory and marker
    particle_trajectory, = ax.plot(
        [], [], [], color="black", linewidth=2, label="Particle Trajectory"
    )
    particle_marker, = ax.plot([], [], [], "o", color="black", markersize=5, label="Particle")

    # Set axis limits and labels
    ax.set_xlim([-0.15, 0.15])
    ax.set_ylim([-0.15, 0.15])
    ax.set_zlim([-0.15, 0.15])
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.legend()

    return fig, ax, arrow_colormap, pole_colormap, particle_trajectory, particle_marker

def add_colorbars(fig, ax, field_norm, arrow_colormap, charge_norm, pole_colormap):
    """
    Adds colorbars for electric field magnitude and electrode charge.
    """
    # Field magnitude colorbar
    field_colorbar = fig.colorbar(
        ScalarMappable(norm=field_norm, cmap=arrow_colormap),
        ax=ax,
        shrink=0.7,
        aspect=15,
        pad=0.1,
    )
    field_colorbar.set_label("Electric Field Magnitude (N/C)")

    # Electrode charge colorbar
    charge_colorbar = fig.colorbar(
        ScalarMappable(norm=charge_norm, cmap=pole_colormap),
        ax=ax,
        shrink=0.7,
        aspect=15,
        pad=0.05,
    )
    charge_colorbar.set_label("Electrode Charge (C/m)")

def update_quiver(ax, X, Y, Z, Ex_total, Ey_total, Ez_total, field_norm, arrow_colormap, quiver):
    """
    Updates the quiver plot for the electric field arrows.
    """
    field_magnitude = (Ex_total**2 + Ey_total**2 + Ez_total**2) ** 0.5
    field_magnitude_normalized = field_norm(field_magnitude)
    colors = arrow_colormap(field_magnitude_normalized.ravel())

    # Remove the previous quiver plot
    if quiver:
        quiver.remove()

    # Create the new quiver plot
    quiver = ax.quiver(
        X, Y, Z,
        Ex_total, Ey_total, Ez_total,
        length=0.01, colors=colors, normalize=True, alpha=0.8
    )

    return quiver