"""Initialize simulation parameters."""
from quadrupole_field.simulation.config import TRAP_CONFIG, PARTICLE_CONFIG
from quadrupole_field.utils.stable_orbit_params import StableOrbitParameters
from quadrupole_field.utils.stability import suggest_diamond_orbit_parameters

def get_initial_parameters() -> StableOrbitParameters:
    """Get the initial parameters for the simulation."""
    return suggest_diamond_orbit_parameters(
        rod_distance=TRAP_CONFIG.rod_distance,
        particle_charge=PARTICLE_CONFIG.charge,
        particle_mass=PARTICLE_CONFIG.mass,
        driving_freq=TRAP_CONFIG.driving_frequency,
    ) 