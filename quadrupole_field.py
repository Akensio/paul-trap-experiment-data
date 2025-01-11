import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.animation import FuncAnimation

# Constants
epsilon_0 = 8.854e-12  # Permittivity of free space (F/m)
lambda_amplitude = 1e-7  # Maximum linear charge density (C/m)
a = 0.1  # Distance of electrodes from origin (m)
omega = 2 * np.pi  # Angular frequency of oscillation (rad/s)

# Define grid for field calculation
grid_size = 25
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

# Function to calculate the electric field due to a single infinite electrode
def calculate_field_from_electrode(X, Y, Z, electrode, lambda_charge):
    Ex, Ey, Ez = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)
    electrode_pos = np.array(electrode['position'])
    
    # Calculate the perpendicular distance to the electrode axis
    R_perp = np.sqrt(
        (X - electrode_pos[0])**2 + (Y - electrode_pos[1])**2
    )
    
    # Electric field magnitude (1/r dependence)
    E_magnitude = (lambda_charge / (2 * np.pi * epsilon_0)) / (R_perp + 1e-9)  # Avoid division by zero
    Ex = E_magnitude * (X - electrode_pos[0]) / (R_perp + 1e-9)
    Ey = E_magnitude * (Y - electrode_pos[1]) / (R_perp + 1e-9)
    # Ez remains zero (no field in the z-direction)
    
    return Ex, Ey, Ez

# Function to update the animation
def update(frame):
    global quiver
    t = frame / 100  # Time step (scale as needed)
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
    
    # Compute the field magnitude and normalize
    field_magnitude = np.sqrt(Ex_total**2 + Ey_total**2 + Ez_total**2)
    field_magnitude_normalized = norm(field_magnitude)
    colors = colormap(field_magnitude_normalized.ravel())
    
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

# Compute field magnitude for consistent normalization
FIELD_MIN = 0
FIELD_MAX = lambda_amplitude / (2 * np.pi * epsilon_0 * 0.1)  # Approximate maximum field
norm = Normalize(vmin=FIELD_MIN, vmax=FIELD_MAX)
colormap = cm.get_cmap('jet')

# Create figure and axes
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot the electrodes
for i, electrode in enumerate(electrodes):
    pos = electrode['position']
    z_range = np.linspace(-0.1, 0.1, 100)  # Infinite approximation
    x_coords = np.full_like(z_range, pos[0])
    y_coords = np.full_like(z_range, pos[1])
    ax.plot(
        x_coords, y_coords, z_range,
        linewidth=3, color='red' if i % 2 == 0 else 'blue'
    )

# Placeholder for quiver plot
quiver = None
skip = 1  # Reduce density of quiver plot

# Add colorbar
scalar_mappable = cm.ScalarMappable(cmap=colormap, norm=norm)
scalar_mappable.set_array([])
cbar = fig.colorbar(scalar_mappable, ax=ax, shrink=0.7, aspect=15, pad=0.1)
cbar.set_label("Electric Field Magnitude (N/C)")

# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=50)

plt.show()