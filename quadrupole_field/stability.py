"""Calculate stable orbit parameters for the Paul trap."""
import numpy as np
from typing import Tuple
from constants import ROD_DISTANCE, PARTICLE_CHARGE, PARTICLE_MASS

def calculate_stability_parameters(
    voltage_amplitude: float,
    driving_frequency: float,
    rod_distance: float,
    charge: float,
    mass: float
) -> Tuple[float, float]:
    """
    Calculate the Mathieu stability parameters.
    Returns (a, q) where:
    - a is the DC stability parameter (0 for pure AC)
    - q is the AC stability parameter
    
    Stable regions typically exist for |q| < 0.908
    """
    omega = 2 * np.pi * driving_frequency
    q = 4 * charge * voltage_amplitude / (mass * omega**2 * rod_distance**2)
    a = 0  # For pure AC operation
    
    return a, q

def suggest_stable_parameters(
    rod_distance: float,
    particle_charge: float,
    particle_mass: float,
    driving_freq: float = 1.0
) -> dict:
    """
    Suggest a set of parameters that should result in stable orbits.
    Returns a dictionary of recommended parameters.
    """
    # Target a q value of about 0.4 (well within stability region)
    target_q = 0.4
    
    omega = 2 * np.pi * driving_freq
    
    # Calculate required voltage for stable operation
    voltage = (target_q * particle_mass * omega**2 * rod_distance**2) / (4 * particle_charge)
    
    # Initial conditions for likely stable orbit
    initial_position = (rod_distance * 0.1, 0.0)  # 10% of rod distance
    initial_velocity = (0.0, 0.0)
    
    return {
        "voltage_amplitude": voltage,
        "driving_frequency": driving_freq,
        "initial_position": initial_position,
        "initial_velocity": initial_velocity,
        "stability_q": target_q
    }

if __name__ == "__main__":
    # Calculate and print suggested parameters
    params = suggest_stable_parameters(
        rod_distance=ROD_DISTANCE,
        particle_charge=PARTICLE_CHARGE,
        particle_mass=PARTICLE_MASS
    )
    print("\nSuggested stable parameters:")
    print(f"Voltage amplitude: {params['voltage_amplitude']:.2f} V")
    print(f"Driving frequency: {params['driving_frequency']:.2f} Hz")
    print(f"Initial position: {params['initial_position']}")
    print(f"Initial velocity: {params['initial_velocity']}")
    print(f"Stability parameter q: {params['stability_q']:.3f}")
    
    # Check if current parameters are stable
    a, q = calculate_stability_parameters(params['voltage_amplitude'], params['driving_frequency'], ROD_DISTANCE, PARTICLE_CHARGE, PARTICLE_MASS)
    print(f"\nStability check:")
    print(f"Current q parameter: {q:.3f}")
    if abs(q) < 0.908:
        print("Parameters are within the primary stability region!")
    else:
        print("Warning: Parameters are outside the primary stability region.") 