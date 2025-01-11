import numpy as np
from trap import Trap
from particle import Particle

class Simulation:
    def __init__(self, a, charge, mass, initial_position, initial_velocity, dt):
        """
        Initialize the simulation with the trap and particle.
        """
        self.trap = Trap(a)
        self.particle = Particle(charge, mass, initial_position, initial_velocity)
        self.dt = dt

    def run(self, voltages_over_time, total_time):
        """
        Run the simulation.
        :param voltages_over_time: Function providing voltages at a given time.
        :param total_time: Total simulation time.
        :return: Lists of particle positions over time.
        """
        positions = []
        time_steps = int(total_time / self.dt)
        for t in range(time_steps):
            t_actual = t * self.dt
            voltages = voltages_over_time(t_actual)
            self.trap.set_voltages(voltages)
            electric_field = self.trap.electric_field_at(
                self.particle.position[0],
                self.particle.position[1]
            )
            self.particle.update(electric_field, self.dt)
            positions.append(self.particle.position.copy())
        return np.array(positions)