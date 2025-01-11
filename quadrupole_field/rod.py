import numpy as np

class Rod:
    def __init__(self, position):
        """
        Initialize a rod.
        :param position: Tuple (x, y) representing the rod's position.
        """
        self.position = np.array(position, dtype=float)
        self.voltage = 0  # Default voltage

    def set_voltage(self, voltage):
        """
        Set the voltage of the rod.
        :param voltage: Voltage value to set.
        """
        self.voltage = voltage

    def electric_field_at(self, x, y):
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