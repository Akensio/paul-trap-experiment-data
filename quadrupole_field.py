import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.animation import FuncAnimation

# Constants
epsilon_0 = 8.854e-12  # Permittivity of free space (F/m)
lambda_amplitude = 1e-7  # Maximum linear charge density (C/m)
a = 0.1  # Distance of electrodes from origin (m)
omega = 2 * np.pi  # Angular frequency of oscillation (rad/s)

# Define grid for field calculation
x = np.linspace(-0.1, 0.1, 10)
y = np.linspace(-0.1, 0.1, 10)
z = np.linspace(-0.1, 0.1, 9)
X, Y, Z = np.meshgrid(x, y, z)

# Define electrode positions
electrodes = [
    {'position': [-a, 0, 0]},  # Electrode at (-a, 0)
    {'position': [a, 0, 0]},   # Electrode at (+a, 0)
    {'position': [0, -a, 0]},  # Electrode at (0, -a)
    {'position': [0, a, 0]},   # Electrode at (0, +a)
]

# Create custom colormaps
# For field arrows: Neutral gradient (gray to lime green)
arrow_colors = [(0, "gray"), (0.5, "cyan"), (1, "blue")]
arrow_colormap = LinearSegmentedColormap.from_list("arrow_colormap", arrow_colors)

# For electrodes: Gradient from yellow (negative) to green (positive)
pole_colors = [(0, "red"), (1, "blue")]
pole_colormap = LinearSegmentedColormap.from_list("pole_colormap", pole_colors)

# Function to calculate the electric field due to a single infinite electrode
def calculate_field_from_electrode(X, Y, Z, electrode, lambda_charge):
    Ex, Ey, Ez = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)
    electrode_pos = np.array(electrode['position'])
    R_perp = np.sqrt((X - electrode_pos[0])**2 + (Y - electrode_pos[1])**2)
    E_magnitude = (lambda_charge / (2 * np.pi * epsilon_0)) / (R_perp + 1e-9)
    Ex = E_magnitude * (X - electrode_pos[0]) / (R_perp + 1e-9)
    Ey = E_magnitude * (Y - electrode_pos[1]) / (R_perp + 1e-9)
    return Ex, Ey, Ez

# Function to update the animation
def update(frame):
    global quiver
    t = frame / 100  # Time step
    lambda_values = [
        lambda_amplitude * np.sin(omega * t),  # Oscillating charge density for electrode 1
        lambda_amplitude * np.sin(omega * t), # Opposite charge density for electrode 2
        -lambda_amplitude * np.sin(omega * t),  # Orthogonal oscillation for electrode 3
        -lambda_amplitude * np.sin(omega * t), # Opposite orthogonal for electrode 4
    ]
    
    Ex_total, Ey_total, Ez_total = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)
    for i, electrode in enumerate(electrodes):
        Ex, Ey, Ez = calculate_field_from_electrode(X, Y, Z, electrode, lambda_values[i])
        Ex_total += Ex
        Ey_total += Ey
        Ez_total += Ez

        # Gradient color for poles
        norm_charge = (lambda_values[i] + lambda_amplitude) / (2 * lambda_amplitude)  # Normalize to [0, 1]
        pole_color = pole_colormap(norm_charge)
        electrode_lines[i].set_color(pole_color)
    
    # Compute the field magnitude and normalize
    field_magnitude = np.sqrt(Ex_total**2 + Ey_total**2 + Ez_total**2)
    field_magnitude_normalized = field_norm(field_magnitude)
    colors = arrow_colormap(field_magnitude_normalized.ravel())
    
    # Clear previous quiver
    if quiver:
        quiver.remove()
    
    # Update quiver plot
    quiver = ax.quiver(
        X[::skip, ::skip, ::skip], Y[::skip, ::skip, ::skip], Z[::skip, ::skip, ::skip],
        Ex_total[::skip, ::skip, ::skip], Ey_total[::skip, ::skip, ::skip], Ez_total[::skip, ::skip, ::skip],
        length=0.01, colors=colors[::skip**3], alpha=0.8, normalize=True
    )
    ax.set_title(f"Electric Field of Quadrupole (t = {t:.2f} s)")

# Compute field normalization for arrows
field_min = 0
field_max = lambda_amplitude / (2 * np.pi * epsilon_0 * 0.1)
field_norm = Normalize(vmin=field_min, vmax=field_max)

# Create figure and axes
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot the electrodes
electrode_lines = []
for electrode in electrodes:
    pos = electrode['position']
    z_range = np.linspace(-0.1, 0.1, 100)
    x_coords = np.full_like(z_range, pos[0])
    y_coords = np.full_like(z_range, pos[1])
    line, = ax.plot(
        x_coords, y_coords, z_range,
        linewidth=3, color='gray'  # Initial neutral color
    )
    electrode_lines.append(line)

# Placeholder for quiver plot
quiver = None
skip = 1

# Add colorbar for field arrows
scalar_mappable = cm.ScalarMappable(cmap=arrow_colormap, norm=field_norm)
scalar_mappable.set_array([])
cbar = fig.colorbar(scalar_mappable, ax=ax, shrink=0.7, aspect=15, pad=0.1)
cbar.set_label("Electric Field Magnitude (N/C)")

# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=50)

plt.show()