from typing import List, Tuple

from quadrupole_field.rod import Rod


class Trap:
    def __init__(self, a: float) -> None:
        """
        Initialize the trap with four rods at (+a, 0), (-a, 0), (0, +a), (0, -a).
        :param a: Distance from the origin to each rod.
        """
        self.rods: List[Rod] = [Rod((a, 0)), Rod((-a, 0)), Rod((0, a)), Rod((0, -a))]

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
