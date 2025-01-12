"""Initialize simulation parameters."""

from quadrupole_field.simulation.config import InitialConditionsConfig
from quadrupole_field.utils.stability import estimate_diamond_orbit_parameters
from quadrupole_field.utils.stable_orbit_params import StableOrbitParameters


def get_initial_parameters(
    rod_distance: float,
    particle_charge: float,
    particle_mass: float,
    driving_freq: float,
    target_q: float,
    initial_conditions: InitialConditionsConfig | None = None,
) -> StableOrbitParameters:
    """Get the initial parameters for the simulation."""
    # Calculate parameters using stability analysis
    calculated = estimate_diamond_orbit_parameters(
        rod_distance=rod_distance,
        particle_charge=particle_charge,
        particle_mass=particle_mass,
        driving_freq=driving_freq,
        target_q=target_q,
    )

    if initial_conditions is None:
        return calculated

    # Use provided overrides, falling back to calculated values when needed
    return StableOrbitParameters(
        voltage_amplitude=initial_conditions.voltage_amplitude
        or calculated.voltage_amplitude,
        driving_frequency=driving_freq,
        initial_position=initial_conditions.get_position()
        or calculated.initial_position,
        initial_velocity=initial_conditions.get_velocity()
        or calculated.initial_velocity,
        stability_q=calculated.stability_q,
        secular_frequency=calculated.secular_frequency,
    )
