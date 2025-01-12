"""Parameters for initializing stable orbits in a Paul trap."""
from dataclasses import dataclass
from typing import Tuple


@dataclass
class StableOrbitParameters:
    """Parameters for initializing a stable particle orbit in the Paul trap.
    
    These parameters are derived from the physical properties of the system:
    - Rod distance (trap geometry)
    - Particle charge
    - Particle mass
    - Driving frequency
    
    They represent a configuration that produces stable particle motion,
    particularly suited for diamond-shaped orbits.
    """
    # Derived driving parameters
    voltage_amplitude: float
    driving_frequency: float
    
    # Calculated initial conditions
    initial_position: Tuple[float, float]
    initial_velocity: Tuple[float, float]
    
    # Resulting stability characteristics
    stability_q: float
    secular_frequency: float 