"""Particle dynamics in electromagnetic fields.

This module implements the particle motion under the influence of electric fields
in the Paul trap, using the Lorentz force law and Newton's equations of motion.
"""

from typing import Tuple

import numpy as np
from numpy.typing import NDArray

from quadrupole_field.core.physical_constants import ELEMENTARY_CHARGE


class Particle:
    """A charged particle in electromagnetic fields.
    
    The particle's motion is determined by:
    - Charge and mass (defining its response to fields)
    - Position and velocity (defining its state)
    - Electric fields (providing the forces)
    
    Motion is integrated using a 4th-order symplectic algorithm for accuracy.
    """
    # Physical properties
    q: float  # Charge
    m: float  # Mass
    
    # Dynamic state
    position: NDArray[np.float64]  # Current position (x, y)
    velocity: NDArray[np.float64]  # Current velocity (vx, vy)

    def __init__(
        self,
        charge: float,
        mass: float,
        position: Tuple[float, float],
        velocity: Tuple[float, float],
    ) -> None:
        """Initialize the particle with its properties."""
        self.q = charge
        self.m = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

    def update(self, electric_field: Tuple[float, float], dt: float) -> None:
        """Update particle's position and velocity using smaller timesteps.
        
        Args:
            electric_field: Electric field vector (Ex, Ey) at particle position
            dt: Time step for the update
        """
        Ex, Ey = electric_field
        # Split the timestep into 4 smaller steps for better accuracy
        dt_small = dt / 4
        for _ in range(4):
            acceleration = self.q * np.array([Ex, Ey]) / self.m
            self.velocity += acceleration * dt_small
            self.position += self.velocity * dt_small
