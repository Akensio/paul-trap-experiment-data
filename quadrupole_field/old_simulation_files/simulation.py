import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Define constants
V_RF = 100       # RF voltage amplitude (V)
omega_RF = 2 * np.pi * 1e6  # RF angular frequency (rad/s)
r_0 = 0.005      # Characteristic distance (m)
q = 1.6e-19      # Charge of the particle (C)
m = 2.18e-25     # Mass of the particle (kg)
g = 9.81         # Gravitational acceleration (m/s^2)
b = 1e-10        # Drag coefficient (kg/s)

# Define the equations of motion
def equations_of_motion_with_drag(t, state):
    x, vx, y, vy = state
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

    # Accelerations
    ax = Fx / m - (b / m) * vx
    ay = Fy / m - (b / m) * vy

    return [vx, ax, vy, ay]

# Initial conditions
initial_x = 1e-6    # Initial x position (m)
initial_y = 2e-6    # Initial y position (m)
initial_vx = 0      # Initial velocity in x (m/s)
initial_vy = 0      # Initial velocity in y (m/s)
initial_state = [initial_x, initial_vx, initial_y, initial_vy]

# Time parameters
t_start = 0
t_end = 1e-4  # Short simulation time to capture oscillations (s)
num_points = 1000
time_eval = np.linspace(t_start, t_end, num_points)

# Solve the equations of motion
print("solving")
solution = solve_ivp(
    equations_of_motion_with_drag,
    [t_start, t_end],
    initial_state,
    t_eval=time_eval,
    method='RK45'
)
print("solved")

# Extract the results
x_vals = solution.y[0]
y_vals = solution.y[2]

# Plot the trajectory in the x-y plane
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_vals, label="Trajectory in x-y plane")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Particle Trajectory in Quadrupole Trap with Air Resistance")
plt.grid(True)
plt.legend()
plt.show()