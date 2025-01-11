import numpy as np
from constants import epsilon_0

def calculate_field_from_electrode(X, Y, Z, electrode_pos, lambda_charge):
    """
    Calculate the electric field components from a single infinite electrode.
    """
    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)
    Ez = np.zeros_like(Z)
    R_perp = ((X - electrode_pos[0]) ** 2 + (Y - electrode_pos[1]) ** 2) ** 0.5
    E_magnitude = (lambda_charge / (2 * np.pi * epsilon_0)) / (R_perp + 1e-9)
    Ex = E_magnitude * (X - electrode_pos[0]) / (R_perp + 1e-9)
    Ey = E_magnitude * (Y - electrode_pos[1]) / (R_perp + 1e-9)
    return Ex, Ey, Ez

def calculate_field_at_point(pos, electrodes, lambda_values):
    """
    Calculates the net electric field at a specific point due to multiple electrodes.
    """
    Ex, Ey, Ez = 0.0, 0.0, 0.0
    for i in range(len(electrodes)):
        electrode_pos = electrodes[i]
        R_perp = np.sqrt(
            (pos[0] - electrode_pos[0]) ** 2 + (pos[1] - electrode_pos[1]) ** 2
        )
        E_magnitude = (lambda_values[i] / (2 * np.pi * epsilon_0)) / (R_perp)
        Ex += E_magnitude * (pos[0] - electrode_pos[0]) / (R_perp)
        Ey += E_magnitude * (pos[1] - electrode_pos[1]) / (R_perp)
    return np.array([Ex, Ey, Ez])