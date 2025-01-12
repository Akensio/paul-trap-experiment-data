"""Calculate stable orbit parameters for the Paul trap."""

import numpy as np

from quadrupole_field.utils.stable_orbit_params import StableOrbitParameters


def calculate_secular_frequency(q: float, driving_freq: float) -> float:
    """Calculate the secular frequency of the trap."""
    return q * driving_freq / (2 * np.sqrt(2))


def estimate_stable_orbit(
    voltage_amplitude: float,
    driving_frequency: float,
    rod_distance: float,
    charge: float,
    mass: float,
) -> tuple[float, float, float]:
    """
    Calculate the Mathieu equation parameters and resulting secular frequency.

    The Mathieu parameters determine the stability of particle motion in a Paul trap:
    - a: DC stability parameter (0 for pure AC operation)
    - q: AC stability parameter (stable trapping typically requires |q| < 0.908)
    - secular_freq: Resulting frequency of the particle's slow oscillation

    For diamond-shaped orbits, q ≈ 0.3-0.4 gives good results.

    Args:
        voltage_amplitude: Peak RF voltage amplitude (V)
        driving_frequency: RF driving frequency (Hz)
        rod_distance: Distance from trap center to rods (m)
        charge: Particle charge (C)
        mass: Particle mass (kg)

    Returns:
        tuple of (a, q, secular_freq)
    """
    omega = 2 * np.pi * driving_frequency
    q = 4 * charge * voltage_amplitude / (mass * omega**2 * rod_distance**2)
    a = 0  # For pure AC operation

    secular_freq = calculate_secular_frequency(q, driving_frequency)
    return a, q, secular_freq


def estimate_diamond_orbit_parameters(
    rod_distance: float,
    particle_charge: float,
    particle_mass: float,
    driving_freq: float,
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

    Returns:
        StableOrbitParameters containing voltage, position, velocity, and stability info
    """
    # Keep the same q for stability
    target_q = 0.3  # Smaller q ensures stability within Mathieu's stability region
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


if __name__ == "__main__":
    """
    TODO: This will be developed into a proper entry point for stability analysis.
    For now, it serves as an example usage of the stability calculations.
    """
    # Example usage with unit values
    params = estimate_diamond_orbit_parameters(
        rod_distance=1.0,
        particle_charge=1.0,
        particle_mass=1.0,
        driving_freq=5.0,
    )

    print("\nSuggested diamond orbit parameters:")
    print(f"Voltage amplitude: {params.voltage_amplitude:.2f} V")
    print(f"Driving frequency: {params.driving_frequency:.2f} Hz")
    print(f"Initial position: {params.initial_position}")
    print(f"Initial velocity: {params.initial_velocity}")
    print(f"Stability parameter q: {params.stability_q:.3f}")
    print(f"Secular frequency: {params.secular_frequency:.2f} Hz")
