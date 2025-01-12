"""Main simulation logic."""

from typing import Callable, List, Tuple

import numpy as np
from numpy.typing import NDArray

from quadrupole_field.core.particle import Particle
from quadrupole_field.core.trap import Trap
from quadrupole_field.simulation.config import SIMULATION_CONFIG


class Simulation:
    def __init__(
        self,
        a: float,
        charge: float,
        mass: float,
        initial_position: Tuple[float, float],
        initial_velocity: Tuple[float, float],
        dt: float,
    ) -> None:
        """Initialize the simulation with the trap and particle."""
        self.trap: Trap = Trap(a)
        self.particle: Particle = Particle(
            charge, mass, initial_position, initial_velocity
        )
        self.dt: float = dt

    def run(
        self, voltages_over_time: Callable[[float], List[float]], total_time: float
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """
        Run the simulation.
        :param voltages_over_time: Function providing voltages at a given time.
        :param total_time: Total simulation time.
        :return: Tuple of (positions, velocities, voltages) over time.
        """
        positions: List[NDArray[np.float64]] = []
        velocities: List[NDArray[np.float64]] = []
        voltages_history: List[List[float]] = []
        time_steps: int = int(total_time / self.dt)

        for t in range(time_steps):
            t_actual = t * self.dt
            voltages = voltages_over_time(t_actual)
            self.trap.set_voltages(voltages)

            electric_field = self.trap.electric_field_at(
                self.particle.position[0], self.particle.position[1]
            )
            self.particle.update(electric_field, self.dt)

            positions.append(self.particle.position.copy())
            velocities.append(self.particle.velocity.copy())
            voltages_history.append(voltages.copy())

        return np.array(positions), np.array(velocities), np.array(voltages_history)
