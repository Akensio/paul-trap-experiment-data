"""Initialize simulation parameters."""
from quadrupole_field.simulation.constants import (
    DRIVING_FREQUENCY,
    PARTICLE_CHARGE,
    PARTICLE_MASS,
    ROD_DISTANCE,
)
from quadrupole_field.utils.stable_orbit_params import StableOrbitParameters
from quadrupole_field.utils.stability import suggest_diamond_orbit_parameters

def get_initial_parameters() -> StableOrbitParameters:
    """Get the initial parameters for the simulation."""
    return suggest_diamond_orbit_parameters(
        rod_distance=ROD_DISTANCE,
        particle_charge=PARTICLE_CHARGE,
        particle_mass=PARTICLE_MASS,
        driving_freq=DRIVING_FREQUENCY,
    ) 