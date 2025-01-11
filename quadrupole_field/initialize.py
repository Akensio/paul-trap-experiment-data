"""Initialize simulation parameters."""

from constants import DRIVING_FREQUENCY, PARTICLE_CHARGE, PARTICLE_MASS, ROD_DISTANCE
from stability import suggest_diamond_orbit_parameters
from orbit_parameters import OrbitParameters

def get_initial_parameters() -> OrbitParameters:
    """Get the initial parameters for the simulation."""
    return suggest_diamond_orbit_parameters(
        rod_distance=ROD_DISTANCE,
        particle_charge=PARTICLE_CHARGE,
        particle_mass=PARTICLE_MASS,
        driving_freq=DRIVING_FREQUENCY,
    )
