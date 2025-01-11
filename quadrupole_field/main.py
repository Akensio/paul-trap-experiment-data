import numpy as np
from typing import List, Tuple
from simulation import Simulation
from plot import animate_simulation


def voltages_over_time(t: float) -> List[float]:
    # Oscillating voltages for rods
    return [
        10 * np.sin(2 * np.pi * t),
        -10 * np.sin(2 * np.pi * t),
        10 * np.cos(2 * np.pi * t),
        -10 * np.cos(2 * np.pi * t),
    ]


if __name__ == "__main__":
    a: float = 1  # Rod distance
    charge: float = 1
    mass: float = 1
    initial_position: Tuple[float, float] = (0.1, 0.1)
    initial_velocity: Tuple[float, float] = (0, 0)
    dt: float = 0.01
    total_time: float = 10

    simulation = Simulation(a, charge, mass, initial_position, initial_velocity, dt)
    positions, voltages_history = simulation.run(voltages_over_time, total_time)

    # Pass positions and voltages to the animation
    animate_simulation(positions, voltages_history, a, simulation.trap, dt)
