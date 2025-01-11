import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import gradio as gr

# Define the equations of motion
def equations_of_motion_with_drag(t, state, V_RF, r_0, omega_RF, q, m, b):
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

    # Accelerations
    ax = Fx / m - (b / m) * vx
    ay = Fy / m - (b / m) * vy

    return [vx, ax, vy, ay]

# Simulation function
def simulate(V_RF, r_0, b, initial_vx, initial_vy, t_end):
    # Constants
    omega_RF = 2 * np.pi * 1e6  # RF angular frequency (rad/s)
    q = 1.6e-19                # Charge of the particle (C)
    m = 2.18e-25               # Mass of the particle (kg)

    # Initial conditions
    initial_x = 1e-6  # Initial x position (m)
    initial_y = 2e-6  # Initial y position (m)
    initial_state = [initial_x, initial_vx, initial_y, initial_vy]

    # Time parameters
    t_start = 0
    num_points = 1000
    time_eval = np.linspace(t_start, t_end, num_points)

    # Solve the equations of motion
    solution = solve_ivp(
        equations_of_motion_with_drag,
        [t_start, t_end],
        initial_state,
        t_eval=time_eval,
        method='LSODA',
        args=(V_RF, r_0, omega_RF, q, m, b)
    )

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
    plt.tight_layout()

    return plt.gcf()

# Create Gradio interface
interface = gr.Interface(
    fn=simulate,
    inputs=[
        gr.Slider(50, 200, step=10, label="V_RF (Voltage Amplitude, V)"),
        gr.Slider(0.001, 0.01, step=0.001, label="r_0 (Characteristic Distance, m)"),
        gr.Slider(1e-12, 1e-8, step=1e-12, label="Drag Coefficient (b, kg/s)"),
        gr.Slider(-1e-5, 1e-5, step=1e-6, label="Initial Velocity in x (m/s)"),
        gr.Slider(-1e-5, 1e-5, step=1e-6, label="Initial Velocity in y (m/s)"),
        gr.Slider(1e-5, 1e-3, step=1e-5, label="Simulation Time (t_end, s)")
    ],
    outputs="plot",
    live=True
)

# Launch the Gradio app
interface.launch()