"""Calculate stable orbit parameters for the Paul trap."""

import numpy as np

from quadrupole_field.utils.stable_orbit_params import StableOrbitParameters


def calculate_secular_frequency(q: float, driving_freq: float) -> float:
    """Calculate the secular frequency of the trap."""
    return q * driving_freq / (2 * np.sqrt(2))


def estimate_diamond_orbit_parameters(
    rod_distance: float,
    particle_charge: float,
    particle_mass: float,
    driving_freq: float,
    target_q: float,
) -> StableOrbitParameters:
    """
    Estimate parameters for a stable diamond-shaped orbit in a Paul trap.

    This function calculates parameters that produce a diamond-shaped orbit, which is
    a characteristic stable motion pattern in Paul traps. The calculation:
    1. Sets q = 0.3 for optimal stability (well within q < 0.908 stability region)
    2. Calculates required voltage based on trap and particle properties
    3. Positions particle at 45° with 8% of rod distance for clear visualization
    4. Sets velocity perpendicular to position for circular secular motion

    Args:
        rod_distance: Distance from trap center to rods (m)
        particle_charge: Charge of the particle (C)
        particle_mass: Mass of the particle (kg)
        driving_freq: RF driving frequency (Hz)
        target_q: Target stability parameter (0 < q < 0.908)

    Returns:
        StableOrbitParameters containing voltage, position, velocity, and stability info
    """
    omega = 2 * np.pi * driving_freq

    # Calculate required voltage for stable operation
    voltage = (target_q * particle_mass * omega**2 * rod_distance**2) / (
        4 * particle_charge
    )

    secular_freq = calculate_secular_frequency(target_q, driving_freq)

    # Keep small initial displacement
    r0 = rod_distance * 0.08  # 8% of rod distance
    angle = np.pi / 4  # 45 degrees

    # Initial position at 45 degrees
    initial_position = (r0 * np.cos(angle), r0 * np.sin(angle))

    # Adjust velocity to match secular frequency
    v0 = 2 * np.pi * secular_freq * r0
    initial_velocity = (-v0 * np.sin(angle), v0 * np.cos(angle))

    return StableOrbitParameters(
        voltage_amplitude=voltage,
        driving_frequency=driving_freq,
        initial_position=initial_position,
        initial_velocity=initial_velocity,
        stability_q=target_q,
        secular_frequency=secular_freq,
    )
