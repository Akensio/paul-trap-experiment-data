"""Configuration settings for the Paul trap simulation.

This module contains all configurable parameters for the simulation, organized into
logical groups. Each parameter can be adjusted to explore different trap behaviors.
"""

from dataclasses import dataclass


@dataclass
class SimulationConfig:
    """Time-related configuration for the simulation.

    Controls the temporal resolution and duration of the simulation. Smaller dt values
    provide more accurate results but increase computation time.
    """

    dt: float = 0.001  # Time step size in seconds
    total_time: float = 5.0  # Total simulation duration in seconds


@dataclass
class TrapConfig:
    """Physical configuration of the trap system.

    Defines the fundamental trap parameters that determine its operation.
    The rod_distance and driving_frequency are key parameters that affect
    particle stability.
    """

    rod_distance: float = 1.0  # Distance from center to rods in meters
    driving_frequency: float = 5.0  # RF frequency in Hz, affects stability


@dataclass
class ParticleConfig:
    """Configuration of the simulated particle.

    Defines the physical properties of the trapped particle. These values
    determine the particle's response to the electric field and its
    stability characteristics.
    """

    charge: float = 1.0  # Particle charge in Coulombs
    mass: float = 1.0  # Particle mass in kilograms


# Create default configuration instances
SIMULATION_CONFIG = SimulationConfig()
TRAP_CONFIG = TrapConfig()
PARTICLE_CONFIG = ParticleConfig()
