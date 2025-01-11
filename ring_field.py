import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.animation import FuncAnimation

# Constants
k = 8.9875517923e9  # Coulomb's constant, N·m²/C²
ring_radius = 1.0  # Radius of the ring, in meters
charge_amplitude = 1e-6  # Maximum charge on the ring, in coulombs
omega = 2 * np.pi  # Angular frequency of oscillation

# Define the ring in 3D space with high resolution
theta = np.linspace(0, 2 * np.pi, 1000)
ring_x = ring_radius * np.cos(theta)
ring_y = ring_radius * np.sin(theta)
ring_z = np.zeros_like(theta)

# Define the grid for field calculation
grid_size = 15
x = np.linspace(-0.5, 0.5, 10)
y = np.linspace(-0.5, 0.5, 10)
z = np.linspace(-0.5, 0.5, 9)
X, Y, Z = np.meshgrid(x, y, z)

# Placeholder for the quiver plot
quiver = None

# Fixed color scale bounds
FIELD_MIN = 0  # Minimum field magnitude for the color scale

# Function to estimate FIELD_MAX
def calculate_field_max():
    Ex_max, Ey_max, Ez_max = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)
    max_charge = charge_amplitude  # Maximum charge
    for t in theta:
        ring_point = np.array([ring_radius * np.cos(t), ring_radius * np.sin(t), 0])
        R = np.stack((X - ring_point[0], Y - ring_point[1], Z - ring_point[2]), axis=0)
        R_magnitude = np.sqrt(np.sum(R**2, axis=0))
        R_unit = R / (R_magnitude + 1e-9)
        dE = k * (max_charge / (2 * np.pi)) * (1 / R_magnitude**2) * R_unit
        Ex_max += dE[0]
        Ey_max += dE[1]
        Ez_max += dE[2]
    
    # Compute maximum magnitude of the field
    field_magnitude_max = np.sqrt(Ex_max**2 + Ey_max**2 + Ez_max**2)
    return np.max(field_magnitude_max)

# Dynamically compute FIELD_MAX
FIELD_MAX = calculate_field_max()
print(f"Calculated FIELD_MAX: {FIELD_MAX}")
# Function to calculate electric field
def calculate_field(charge):
    Ex, Ey, Ez = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)
    for t in theta:
        ring_point = np.array([ring_radius * np.cos(t), ring_radius * np.sin(t), 0])
        R = np.stack((X - ring_point[0], Y - ring_point[1], Z - ring_point[2]), axis=0)
        R_magnitude = np.sqrt(np.sum(R**2, axis=0))
        R_unit = R / (R_magnitude + 1e-9)
        dE = k * (charge / (2 * np.pi)) * (1 / R_magnitude**2) * R_unit
        Ex += dE[0]
        Ey += dE[1]
        Ez += dE[2]
    return Ex, Ey, Ez

# Function to update the animation
def update(frame):
    global quiver
    charge = charge_amplitude * np.sin(omega * frame / 50)  # Oscillating charge
    Ex, Ey, Ez = calculate_field(charge)
    field_magnitude = np.sqrt(Ex**2 + Ey**2 + Ez**2)
    
    # Normalize field magnitudes using fixed scale
    field_magnitude_normalized = (field_magnitude - FIELD_MIN) / (FIELD_MAX - FIELD_MIN)
    field_magnitude_normalized = np.clip(field_magnitude_normalized, 0, 1)  # Ensure values are in [0, 1]
    
    # Map magnitudes to colors using the fixed scale
    colors = cm.jet(field_magnitude_normalized.ravel())
    
    # Clear previous quiver
    if quiver:
        quiver.remove()
    
    # Update quiver plot
    quiver = ax.quiver(
        X, Y, Z, Ex, Ey, Ez,
        length=0.05, colors=colors, alpha=0.8, normalize=True
    )
    ax.set_title(f"Electric Field Around a Charged Ring (Time: {frame})")

# Create a figure and 3D axes
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot the charged ring
ax.plot(ring_x, ring_y, ring_z, color='red', linewidth=2, label="Charged Ring")
ax.legend()

# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=50)

plt.show()