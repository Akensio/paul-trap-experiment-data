"""Initialize simulation parameters."""

from quadrupole_field.simulation.config import DEFAULT_PARTICLE_CONFIG, DEFAULT_TRAP_CONFIG
from quadrupole_field.utils.stability import estimate_diamond_orbit_parameters
from quadrupole_field.utils.stable_orbit_params import StableOrbitParameters


def get_initial_parameters(
    rod_distance: float = DEFAULT_TRAP_CONFIG.rod_distance,
    particle_charge: float = DEFAULT_PARTICLE_CONFIG.charge,
    particle_mass: float = DEFAULT_PARTICLE_CONFIG.mass,
    driving_freq: float = DEFAULT_TRAP_CONFIG.driving_frequency,
) -> StableOrbitParameters:
    """Get the initial parameters for the simulation."""
    return estimate_diamond_orbit_parameters(
        rod_distance=rod_distance,
        particle_charge=particle_charge,
        particle_mass=particle_mass,
        driving_freq=driving_freq,
    )
