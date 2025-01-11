import numpy as np
import matplotlib.pyplot as plt

# Define constants
V_RF = 100       # RF voltage amplitude (V)
omega_RF = 2 * np.pi * 1e6  # RF angular frequency (rad/s)
r_0 = 0.005      # Characteristic distance (m)
q = 1.6e-19      # Charge of the particle (C)
m = 2.18e-25     # Mass of the particle (kg)
g = 9.81         # Gravitational acceleration (m/s^2)

# Define the force components as functions of position (x, y)
def force_field(x, y, t):
    t_dependence = np.cos(omega_RF * t)

    # Forces in x-direction
    Fx = -q * (
        V_RF * t_dependence * ((x - r_0) / ((x - r_0)**2 + y**2)**1.5 +
                               (x + r_0) / ((x + r_0)**2 + y**2)**1.5) -
        V_RF * t_dependence * (x / (x**2 + (y - r_0)**2)**1.5 +
                               x / (x**2 + (y + r_0)**2)**1.5)
    )
    
    # Forces in y-direction
    Fy = -q * (
        V_RF * t_dependence * (y / ((x - r_0)**2 + y**2)**1.5 +
                               y / ((x + r_0)**2 + y**2)**1.5) -
        V_RF * t_dependence * ((y - r_0) / (x**2 + (y - r_0)**2)**1.5 +
                               (y + r_0) / (x**2 + (y + r_0)**2)**1.5)
    )
    Fy += m * g  # Add gravitational force

    return Fx, Fy

# Generate a grid of points in the x-y plane
x_vals = np.linspace(-1e-3, 1e-3, 20)  # x range
y_vals = np.linspace(-1e-3, 1e-3, 20)  # y range
x_grid, y_grid = np.meshgrid(x_vals, y_vals)

# Calculate forces at each grid point at t = 0 (example time)
t_example = 0
Fx_grid = np.zeros_like(x_grid)
Fy_grid = np.zeros_like(y_grid)

# Loop through grid points to calculate forces
for i in range(len(x_vals)):
    for j in range(len(y_vals)):
        Fx, Fy = force_field(x_grid[i, j], y_grid[i, j], t_example)
        Fx_grid[i, j] = Fx
        Fy_grid[i, j] = Fy

# Normalize the forces for visualization
magnitude = np.sqrt(Fx_grid**2 + Fy_grid**2)
Fx_grid_normalized = Fx_grid / magnitude
Fy_grid_normalized = Fy_grid / magnitude

# Create a quiver plot
plt.figure(figsize=(8, 6))
plt.quiver(x_grid, y_grid, Fx_grid_normalized, Fy_grid_normalized, magnitude, scale=20, cmap='viridis')
plt.colorbar(label="Force Magnitude (N)")
plt.title("Force Field in the x-y Plane")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid(True)
plt.show()