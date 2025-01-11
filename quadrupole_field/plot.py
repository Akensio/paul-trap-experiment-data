import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate_simulation(positions, a):
    """
    Animate the particle's trajectory over time in the Paul trap.
    :param positions: Array of particle positions over time.
    :param a: Rod distance from the origin.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1.5 * a, 1.5 * a)
    ax.set_ylim(-1.5 * a, 1.5 * a)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Particle Trajectory in Paul Trap (Animation)")
    ax.grid()

    # Plot the rods
    ax.plot([a, -a, 0, 0], [0, 0, a, -a], 'ro', label="Rods")
    ax.legend()

    # Particle's current position
    particle_dot, = ax.plot([], [], 'bo', label="Particle")
    trajectory_line, = ax.plot([], [], 'b-', lw=1, label="Trajectory")

    # Initialize the animation
    def init():
        particle_dot.set_data([], [])
        trajectory_line.set_data([], [])
        return particle_dot, trajectory_line

    # Update function for each frame
    def update(frame):
        x, y = positions[:frame, 0], positions[:frame, 1]
        particle_dot.set_data([x[-1]], [y[-1]])  # Update particle position
        trajectory_line.set_data(x, y)          # Update trajectory
        return particle_dot, trajectory_line

    # Create the animation
    anim = FuncAnimation(fig, update, frames=len(positions), init_func=init, blit=True, interval=20)

    # Show the animation
    plt.show()