from typing import Tuple

import numpy as np
from numpy.typing import NDArray


class Particle:
    def __init__(
        self,
        charge: float,
        mass: float,
        position: Tuple[float, float],
        velocity: Tuple[float, float],
    ) -> None:
        """
        Initialize the particle with its properties.
        :param charge: Charge of the particle.
        :param mass: Mass of the particle.
        :param position: Initial position as a tuple (x, y).
        :param velocity: Initial velocity as a tuple (vx, vy).
        """
        self.q: float = charge
        self.m: float = mass
        self.position: NDArray[np.float64] = np.array(position, dtype=float)
        self.velocity: NDArray[np.float64] = np.array(velocity, dtype=float)

    def update(self, electric_field: Tuple[float, float], dt: float) -> None:
        """
        Update the particle's position and velocity.
        :param electric_field: Electric field vector (Ex, Ey).
        :param dt: Time step.
        """
        Ex, Ey = electric_field
        acceleration = self.q * np.array([Ex, Ey]) / self.m
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
