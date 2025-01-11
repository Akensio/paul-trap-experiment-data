"""Initialize simulation parameters."""
from constants import (
    ROD_DISTANCE,
    PARTICLE_CHARGE,
    PARTICLE_MASS,
    DRIVING_FREQUENCY
)
from stability import suggest_diamond_orbit_parameters

def get_initial_parameters():
    """Get the initial parameters for the simulation."""
    params = suggest_diamond_orbit_parameters(
        rod_distance=ROD_DISTANCE,
        particle_charge=PARTICLE_CHARGE,
        particle_mass=PARTICLE_MASS,
        driving_freq=DRIVING_FREQUENCY
    )
    
    return params 