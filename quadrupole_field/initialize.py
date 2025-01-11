"""Initialize simulation parameters."""

from quadrupole_field.constants import (
    DRIVING_FREQUENCY,
    PARTICLE_CHARGE,
    PARTICLE_MASS,
    ROD_DISTANCE,
)
from quadrupole_field.stability import suggest_diamond_orbit_parameters
from quadrupole_field.orbit_parameters import OrbitParameters

def get_initial_parameters() -> OrbitParameters:
    """Get the initial parameters for the simulation."""
    return suggest_diamond_orbit_parameters(
        rod_distance=ROD_DISTANCE,
        particle_charge=PARTICLE_CHARGE,
        particle_mass=PARTICLE_MASS,
        driving_freq=DRIVING_FREQUENCY,
    )
