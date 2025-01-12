"""Rod component for the Paul trap.

This module defines the Rod class, which represents a single electrode in the Paul trap.
Each rod contributes to the total electric field and can have its voltage varied over time.
"""

from typing import Tuple

import numpy as np
from numpy.typing import NDArray


class Rod:
    """A single electrode rod in the Paul trap.

    The rod is modeled as a point charge for field calculations, with its
    contribution to the electric field falling off as 1/r from its position.
    """

    position: NDArray[np.float64]
    voltage: float

    def __init__(self, position: Tuple[float, float]) -> None:
        """
        Initialize a rod.
        :param position: Tuple (x, y) representing the rod's position.
        """
        self.position = np.array(position, dtype=float)
        self.voltage = 0.0

    def set_voltage(self, voltage: float) -> None:
        """
        Set the voltage of the rod.
        :param voltage: Voltage value to set.
        """
        self.voltage = voltage

    def electric_field_at(self, x: float, y: float) -> Tuple[float, float]:
        """
        Calculate the electric field contribution at a point (x, y).
        :param x: X-coordinate of the point.
        :param y: Y-coordinate of the point.
        :return: Electric field vector (Ex, Ey).
        """
        dx, dy = x - self.position[0], y - self.position[1]
        R = np.sqrt(dx**2 + dy**2) + 1e-9  # Avoid division by zero
        E_magnitude = self.voltage / R
        Ex = E_magnitude * (dx / R)
        Ey = E_magnitude * (dy / R)
        return Ex, Ey
