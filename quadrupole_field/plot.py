import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def animate_simulation(positions, a, trap, field_resolution=20):
    """
    Animate the particle's trajectory over time in the Paul trap, with a quiver plot of the electric field.
    :param positions: Array of particle positions over time.
    :param a: Rod distance from the origin.
    :param trap: The trap object containing the rods.
    :param field_resolution: Number of grid points along one axis for the quiver plot.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1.5 * a, 1.5 * a)
    ax.set_ylim(-1.5 * a, 1.5 * a)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Particle Trajectory in Paul Trap (Animation with Field)")
    ax.grid()

    # Plot the rods
    ax.plot([a, -a, 0, 0], [0, 0, a, -a], 'ro', label="Rods")
    ax.legend()

    # Particle's current position
    particle_dot, = ax.plot([], [], 'bo', label="Particle")
    trajectory_line, = ax.plot([], [], 'b-', lw=1, label="Trajectory")

    # Set up the quiver grid
    x = np.linspace(-1.5 * a, 1.5 * a, field_resolution)
    y = np.linspace(-1.5 * a, 1.5 * a, field_resolution)
    X, Y = np.meshgrid(x, y)
    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)
    quiver = ax.quiver(X, Y, Ex, Ey, color='gray', alpha=0.6)

    # Initialize the animation
    def init():
        particle_dot.set_data([], [])
        trajectory_line.set_data([], [])
        quiver.set_UVC(Ex, Ey)  # Initialize quiver with zero vectors
        return particle_dot, trajectory_line, quiver

    # Update function for each frame
    def update(frame):
        # Particle trajectory
        x_traj, y_traj = positions[:frame, 0], positions[:frame, 1]
        particle_dot.set_data([x_traj[-1]], [y_traj[-1]])  # Update particle position
        trajectory_line.set_data(x_traj, y_traj)           # Update trajectory

        # Update quiver plot (electric field vectors)
        voltages = trap.rods[0].voltage, trap.rods[1].voltage, trap.rods[2].voltage, trap.rods[3].voltage
        for i in range(len(X)):
            for j in range(len(Y)):
                Ex[i, j], Ey[i, j] = trap.electric_field_at(X[i, j], Y[i, j])
        quiver.set_UVC(Ex, Ey)  # Update quiver vectors

        return particle_dot, trajectory_line, quiver

    # Create the animation
    anim = FuncAnimation(fig, update, frames=len(positions), init_func=init, blit=True, interval=20)

    # Show the animation
    plt.show()