"""Main simulation runner."""
from typing import List
import numpy as np

from quadrupole_field.simulation.config import SIMULATION_CONFIG
from quadrupole_field.simulation.constants import (
    DRIVING_FREQUENCY,
    PARTICLE_CHARGE,
    PARTICLE_MASS,
    ROD_DISTANCE,
)
from quadrupole_field.utils.initialization import get_initial_parameters
from quadrupole_field.utils.orbit import OrbitParameters
from quadrupole_field.visualization.visualizer import PaulTrapVisualizer
from quadrupole_field.simulation.simulation import Simulation

# Get initial parameters with the new diamond orbit calculations
params: OrbitParameters = get_initial_parameters()

def voltages_over_time(t: float) -> List[float]:
    """Calculate oscillating voltages for rods at time t."""
    voltage = params.voltage_amplitude * np.sin(
        2 * np.pi * params.driving_frequency * t
    )
    return [voltage, voltage, -voltage, -voltage]

if __name__ == "__main__":
    # Print initial conditions for debugging
    print(f"Initial conditions:")
    print(f"Voltage amplitude: {params.voltage_amplitude:.2f} V")
    print(f"Initial position: {params.initial_position}")
    print(f"Initial velocity: {params.initial_velocity}")

    simulation = Simulation(
        a=ROD_DISTANCE,
        charge=PARTICLE_CHARGE,
        mass=PARTICLE_MASS,
        initial_position=params.initial_position,
        initial_velocity=params.initial_velocity,
        dt=SIMULATION_CONFIG.dt,
    )

    positions, velocities, voltages_history = simulation.run(
        voltages_over_time, SIMULATION_CONFIG.total_time
    )

    visualizer = PaulTrapVisualizer(
        positions=positions,
        velocities=velocities,
        voltages_history=voltages_history,
        a=ROD_DISTANCE,
        trap=simulation.trap,
        dt=SIMULATION_CONFIG.dt,
    )

    # Save video and show animation
    visualizer.animate(save_video=False, filename="out/paul_trap_simulation.mp4")
