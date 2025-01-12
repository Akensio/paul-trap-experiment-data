"""Main simulation runner."""

import numpy as np

from quadrupole_field.simulation.simulation import Simulation
from quadrupole_field.utils.cli import parse_args
from quadrupole_field.utils.initialization import get_initial_parameters
from quadrupole_field.visualization.paul_trap_display import PaulTrapVisualizer


def main() -> None:
    """Run the Paul trap simulation with command line arguments."""
    # Parse command line arguments
    sim_config, trap_config, particle_config, output_config, initial_config = (
        parse_args()
    )

    # Get initial parameters with optional overrides
    params = get_initial_parameters(
        rod_distance=trap_config.rod_distance,
        particle_charge=particle_config.charge,
        particle_mass=particle_config.mass,
        driving_freq=trap_config.driving_frequency,
        initial_conditions=initial_config,
    )

    def voltages_over_time(t: float) -> list[float]:
        """Calculate oscillating voltages for rods at time t."""
        voltage = params.voltage_amplitude * np.sin(
            2 * np.pi * params.driving_frequency * t
        )
        return [voltage, voltage, -voltage, -voltage]

    # Print initial conditions
    print(f"\nInitial conditions:")
    print(f"Voltage amplitude: {params.voltage_amplitude:.2f} V")
    print(f"Initial position: {params.initial_position}")
    print(f"Initial velocity: {params.initial_velocity}")

    # Run simulation
    simulation = Simulation(
        a=trap_config.rod_distance,
        charge=particle_config.charge,
        mass=particle_config.mass,
        initial_position=params.initial_position,
        initial_velocity=params.initial_velocity,
        dt=sim_config.dt,
    )

    positions, velocities, voltages_history = simulation.run(
        voltages_over_time, sim_config.total_time
    )

    # Visualize results
    visualizer = PaulTrapVisualizer(
        positions=positions,
        velocities=velocities,
        voltages_history=voltages_history,
        a=trap_config.rod_distance,
        trap=simulation.trap,
        dt=sim_config.dt,
    )

    visualizer.animate(
        save_video=output_config.save_video,
        filename=output_config.output_file,
    )


if __name__ == "__main__":
    main()
