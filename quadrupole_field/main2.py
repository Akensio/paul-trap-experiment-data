import numpy as np

from plot import plot_simulation
from simulation import Simulation


def voltages_over_time(t):
    # Oscillating voltages for rods
    return [10 * np.sin(2 * np.pi * t), -10 * np.sin(2 * np.pi * t),
            10 * np.cos(2 * np.pi * t), -10 * np.cos(2 * np.pi * t)]

if __name__ == "__main__":
    rod_positions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    a = 1
    charge = 1
    mass = 1
    initial_position = (0.1, 0.1)
    initial_velocity = (0, 0)
    dt = 0.01
    total_time = 10

    simulation = Simulation(rod_positions, a, charge, mass, initial_position, initial_velocity, dt)
    positions = simulation.run(voltages_over_time, total_time)
    plot_simulation(rod_positions, a, positions)