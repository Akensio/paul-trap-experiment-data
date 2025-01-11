import matplotlib.pyplot as plt
import numpy as np


def plot_simulation(rod_positions, a, positions):
    """
    Plot the particle trajectory and rod positions.
    :param rod_positions: Rod positions.
    :param a: Rod spacing.
    :param positions: Particle positions over time.
    """
    x, y = positions[:, 0], positions[:, 1]
    plt.figure(figsize=(8, 8))
    for rod_x, rod_y in rod_positions:
        plt.plot(
            rod_x, rod_y, "ro", label="Rod" if rod_x == rod_positions[0][0] else ""
        )
    plt.plot(x, y, label="Particle Trajectory")
    plt.xlim(-1.5 * a, 1.5 * a)
    plt.ylim(-1.5 * a, 1.5 * a)
    plt.legend()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Particle Trajectory in Paul Trap")
    plt.grid()
    plt.show()
