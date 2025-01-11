import numpy as np


class ElectricField:
    def __init__(self, rod_positions, a):
        """
        Initialize the field with rod positions.
        :param rod_positions: List of tuples for rod positions (x, y).
        :param a: Distance from origin to each rod.
        """
        self.rod_positions = rod_positions
        self.a = a

    def compute_field(self, x, y, voltages):
        """
        Compute the electric field at point (x, y).
        :param x: X-coordinate of the point.
        :param y: Y-coordinate of the point.
        :param voltages: List of voltages applied to each rod.
        :return: Electric field vector (Ex, Ey).
        """
        Ex, Ey = 0, 0
        for i, (rod_x, rod_y) in enumerate(self.rod_positions):
            dx, dy = x - rod_x, y - rod_y
            R = np.sqrt(dx**2 + dy**2) + 1e-9  # Avoid division by zero
            E_magnitude = voltages[i] / R
            Ex += E_magnitude * (dx / R)
            Ey += E_magnitude * (dy / R)
        return Ex, Ey