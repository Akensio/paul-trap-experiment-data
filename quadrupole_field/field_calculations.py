# field_calculations.py

import numpy as np
from constants import epsilon_0

def calculate_field_from_electrode(X, Y, Z, electrode, lambda_charge):
    Ex, Ey, Ez = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)
    electrode_pos = np.array(electrode["position"])
    R_perp = np.sqrt((X - electrode_pos[0]) ** 2 + (Y - electrode_pos[1]) ** 2)
    E_magnitude = (lambda_charge / (2 * np.pi * epsilon_0)) / (R_perp + 1e-9)
    Ex = E_magnitude * (X - electrode_pos[0]) / (R_perp + 1e-9)
    Ey = E_magnitude * (Y - electrode_pos[1]) / (R_perp + 1e-9)
    return Ex, Ey, Ez

def calculate_field_at_point(pos, electrodes, lambda_values):
    Ex, Ey, Ez = 0, 0, 0
    for i, electrode in enumerate(electrodes):
        electrode_pos = np.array(electrode["position"])
        R_perp = np.sqrt(
            (pos[0] - electrode_pos[0]) ** 2 + (pos[1] - electrode_pos[1]) ** 2
        )
        E_magnitude = (lambda_values[i] / (2 * np.pi * epsilon_0)) / (R_perp + 1e-9)
        Ex += E_magnitude * (pos[0] - electrode_pos[0]) / (R_perp + 1e-9)
        Ey += E_magnitude * (pos[1] - electrode_pos[1]) / (R_perp + 1e-9)
    return np.array([Ex, Ey, Ez])