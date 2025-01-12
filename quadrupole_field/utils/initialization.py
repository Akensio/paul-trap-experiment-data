"""Initialize simulation parameters."""

from quadrupole_field.simulation.config import PARTICLE_CONFIG, TRAP_CONFIG
from quadrupole_field.utils.stability import estimate_diamond_orbit_parameters
from quadrupole_field.utils.stable_orbit_params import StableOrbitParameters


def get_initial_parameters() -> StableOrbitParameters:
    """Get the initial parameters for the simulation."""
    return estimate_diamond_orbit_parameters(
        rod_distance=TRAP_CONFIG.rod_distance,
        particle_charge=PARTICLE_CONFIG.charge,
        particle_mass=PARTICLE_CONFIG.mass,
        driving_freq=TRAP_CONFIG.driving_frequency,
    )
