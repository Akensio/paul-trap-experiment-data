"""Particle physics component."""

from typing import Tuple

import numpy as np
from numpy.typing import NDArray

from quadrupole_field.core.physical_constants import ELEMENTARY_CHARGE


class Particle:
    def __init__(
        self,
        charge: float,
        mass: float,
        position: Tuple[float, float],
        velocity: Tuple[float, float],
    ) -> None:
        """Initialize the particle with its properties."""
        self.q: float = charge
        self.m: float = mass
        self.position: NDArray[np.float64] = np.array(position, dtype=float)
        self.velocity: NDArray[np.float64] = np.array(velocity, dtype=float)

    def update(self, electric_field: Tuple[float, float], dt: float) -> None:
        """Update particle's position and velocity using smaller timesteps."""
        Ex, Ey = electric_field
        # Split the timestep into 4 smaller steps for better accuracy
        dt_small = dt / 4
        for _ in range(4):
            acceleration = self.q * np.array([Ex, Ey]) / self.m
            self.velocity += acceleration * dt_small
            self.position += self.velocity * dt_small
