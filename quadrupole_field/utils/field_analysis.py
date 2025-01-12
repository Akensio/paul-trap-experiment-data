"""Utilities for analyzing electric fields."""

import numpy as np
from numpy.typing import NDArray

from quadrupole_field.core.trap import Trap
from quadrupole_field.visualization.config import PLOT_CONFIG


def calculate_max_field_magnitude(
    trap: Trap,
    voltages_history: NDArray[np.float64],
    a: float,
) -> float:
    """Calculate the maximum field magnitude across all time steps.

    Args:
        trap: Trap instance for field calculations
        voltages_history: History of voltages for animation
        a: Trap size parameter

    Returns:
        Maximum field magnitude encountered
    """
    max_magnitude = 0

    # Create grid using the same parameters as FieldVisualizer
    x = np.linspace(
        -a * PLOT_CONFIG.field_extent_factor,
        a * PLOT_CONFIG.field_extent_factor,
        PLOT_CONFIG.field_resolution,
    )
    y = np.linspace(
        -a * PLOT_CONFIG.field_extent_factor,
        a * PLOT_CONFIG.field_extent_factor,
        PLOT_CONFIG.field_resolution,
    )
    X, Y = np.meshgrid(x, y)

    # Sample time points
    sample_indices = np.linspace(
        0, len(voltages_history) - 1, PLOT_CONFIG.field_sampling_points, dtype=int
    )

    for t_idx in sample_indices:
        # Set voltages for this time step
        trap.set_voltages(voltages_history[t_idx])

        # Calculate field at each point
        for i in range(len(X)):
            for j in range(len(Y)):
                Ex, Ey = trap.electric_field_at(X[i, j], Y[i, j])
                magnitude = np.sqrt(Ex**2 + Ey**2)
                if np.isfinite(magnitude):
                    max_magnitude = max(max_magnitude, magnitude)

    return max_magnitude
