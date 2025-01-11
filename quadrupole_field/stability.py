"""Calculate stable orbit parameters for the Paul trap."""

from typing import Tuple

import numpy as np


def calculate_secular_frequency(q: float, driving_freq: float) -> float:
    """
    Calculate the secular frequency of the trap.
    For small q, Ω ≈ (q/√8)ω where ω is the driving frequency
    """
    omega = 2 * np.pi * driving_freq
    return (q / np.sqrt(8)) * omega


def calculate_stability_parameters(
    voltage_amplitude: float,
    driving_frequency: float,
    rod_distance: float,
    charge: float,
    mass: float,
) -> Tuple[float, float, float]:
    """
    Calculate the Mathieu stability parameters and secular frequency.
    Returns (a, q, secular_freq) where:
    - a is the DC stability parameter (0 for pure AC)
    - q is the AC stability parameter
    - secular_freq is the secular frequency in Hz

    For diamond motion, we want q ≈ 0.4-0.5
    """
    omega = 2 * np.pi * driving_frequency
    q = 4 * charge * voltage_amplitude / (mass * omega**2 * rod_distance**2)
    a = 0  # For pure AC operation

    secular_freq = calculate_secular_frequency(q, driving_frequency)
    return a, q, secular_freq


def suggest_diamond_orbit_parameters(
    rod_distance: float,
    particle_charge: float,
    particle_mass: float,
    driving_freq: float,
) -> dict:
    """
    Suggest parameters for a diamond-shaped orbit.
    Returns a dictionary of recommended parameters.
    """
    # Keep the same q for stability
    target_q = 0.3

    omega = 2 * np.pi * driving_freq

    # Calculate required voltage for stable operation
    voltage = (target_q * particle_mass * omega**2 * rod_distance**2) / (
        4 * particle_charge
    )

    # Calculate secular frequency
    secular_freq = calculate_secular_frequency(target_q, driving_freq)

    # Keep small initial displacement
    r0 = rod_distance * 0.08  # 8% of rod distance
    angle = np.pi / 4  # 45 degrees

    # Initial position at 45 degrees
    initial_position = (r0 * np.cos(angle), r0 * np.sin(angle))

    # Adjust velocity to match secular frequency
    v0 = 2 * np.pi * secular_freq * r0 * 0.8  # Increased factor for more momentum
    initial_velocity = (-v0 * np.sin(angle), v0 * np.cos(angle))

    return {
        "voltage_amplitude": voltage,
        "driving_frequency": driving_freq,
        "initial_position": initial_position,
        "initial_velocity": initial_velocity,
        "stability_q": target_q,
        "secular_frequency": secular_freq,
    }


if __name__ == "__main__":
    # Example usage with unit values
    params = suggest_diamond_orbit_parameters(
        rod_distance=1.0, particle_charge=1.0, particle_mass=1.0
    )

    print("\nSuggested diamond orbit parameters:")
    print(f"Voltage amplitude: {params['voltage_amplitude']:.2f} V")
    print(f"Driving frequency: {params['driving_frequency']:.2f} Hz")
    print(f"Initial position: {params['initial_position']}")
    print(f"Initial velocity: {params['initial_velocity']}")
    print(f"Stability parameter q: {params['stability_q']:.3f}")
    print(f"Secular frequency: {params['secular_frequency']:.2f} Hz")
