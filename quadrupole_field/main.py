from typing import List

import numpy as np
from config import SIMULATION_CONFIG
from constants import DRIVING_FREQUENCY, PARTICLE_CHARGE, PARTICLE_MASS, ROD_DISTANCE
from initialize import get_initial_parameters
from plot import PaulTrapVisualizer
from simulation import Simulation

# Get initial parameters with the new diamond orbit calculations
params = get_initial_parameters()
VOLTAGE_AMPLITUDE = params["voltage_amplitude"]
INITIAL_POSITION = params["initial_position"]
INITIAL_VELOCITY = params["initial_velocity"]


def voltages_over_time(t: float) -> List[float]:
    """Calculate oscillating voltages for rods at time t."""
    voltage = VOLTAGE_AMPLITUDE * np.sin(2 * np.pi * DRIVING_FREQUENCY * t)
    return [voltage, voltage, -voltage, -voltage]


if __name__ == "__main__":
    # Print initial conditions for debugging
    print(f"Initial conditions:")
    print(f"Voltage amplitude: {VOLTAGE_AMPLITUDE:.2f} V")
    print(f"Initial position: {INITIAL_POSITION}")
    print(f"Initial velocity: {INITIAL_VELOCITY}")

    simulation = Simulation(
        a=ROD_DISTANCE,
        charge=PARTICLE_CHARGE,
        mass=PARTICLE_MASS,
        initial_position=INITIAL_POSITION,
        initial_velocity=INITIAL_VELOCITY,
        dt=SIMULATION_CONFIG.dt,
    )

    positions, voltages_history = simulation.run(
        voltages_over_time, SIMULATION_CONFIG.total_time
    )

    visualizer = PaulTrapVisualizer(
        positions=positions,
        voltages_history=voltages_history,
        a=ROD_DISTANCE,
        trap=simulation.trap,
        dt=SIMULATION_CONFIG.dt,
    )
    visualizer.animate()
