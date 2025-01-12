from typing import List, Tuple

from quadrupole_field.core.rod import Rod

"""Core trap physics implementation.

This module implements the quadrupole Paul trap geometry and field calculations.
The trap consists of four rods arranged in a square configuration, with
time-varying voltages creating the trapping field.
"""


class Trap:
    """Quadrupole Paul trap implementation.

    The trap consists of four rods arranged in a square pattern:
    - Two rods on the x-axis at ±a
    - Two rods on the y-axis at ±a
    where 'a' is the distance from the center to each rod.
    """

    rods: List[Rod]

    def __init__(self, a: float) -> None:
        """Initialize the trap with four rods."""
        self.rods = [Rod((a, 0)), Rod((-a, 0)), Rod((0, a)), Rod((0, -a))]

    def set_voltages(self, voltages: List[float]) -> None:
        """
        Set voltages for all rods.
        :param voltages: List of 4 voltage values, one for each rod.
        """
        if len(voltages) != 4:
            raise ValueError("Exactly 4 voltages must be provided.")
        for rod, voltage in zip(self.rods, voltages):
            rod.set_voltage(voltage)

    def electric_field_at(self, x: float, y: float) -> Tuple[float, float]:
        """
        Calculate the total electric field at a point (x, y) due to all rods.
        :param x: X-coordinate of the point.
        :param y: Y-coordinate of the point.
        :return: Total electric field vector (Ex, Ey).
        """
        Ex, Ey = 0, 0
        for rod in self.rods:
            Ex_rod, Ey_rod = rod.electric_field_at(x, y)
            Ex += Ex_rod
            Ey += Ey_rod
        return Ex, Ey
