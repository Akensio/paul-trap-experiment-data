"""Rod component for the Paul trap.

This module defines the Rod class, which represents a single electrode in the Paul trap.
Each rod contributes to the total electric field and can have its voltage varied over time.
"""

import numpy as np
from numpy.typing import NDArray


class Rod:
    """A single electrode rod in the Paul trap.

    The rod is modeled as an infinite line charge for field calculations, with its
    contribution to the electric field falling off as 1/r from its position.
    """

    position: NDArray[np.float64]
    voltage: float

    def __init__(self, position: tuple[float, float]) -> None:
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

    def electric_field_at(self, x: float, y: float) -> tuple[float, float]:
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

    def electric_potential_at(
        self, x: float, y: float, min_distance: float = 1e-9
    ) -> float:
        """Calculate the electric potential at a point due to this rod.

        For an infinite line charge, the potential follows:
            V(r) = -(λ/2πε₀) * ln(r/r₀)
        where:
            λ is the charge density (proportional to voltage here)
            r is the distance from the line
            r₀ is a reference distance

        Args:
            x: X-coordinate of the point
            y: Y-coordinate of the point
            min_distance: Minimum distance threshold to prevent singularities

        Returns:
            Electric potential value at the given point
        """
        dx = x - self.position[0]
        dy = y - self.position[1]
        R = np.sqrt(dx**2 + dy**2) + min_distance
        return -self.voltage * np.log(
            R
        )  # Negative because higher voltage = lower potential
