"""Configuration settings for the Paul trap simulation."""
from dataclasses import dataclass


@dataclass
class SimulationConfig:
    """Time-related configuration for the simulation."""
    dt: float = 0.001  # Time step size
    total_time: float = 5.0  # Total simulation duration


@dataclass
class TrapConfig:
    """Physical configuration of the trap system."""
    rod_distance: float = 1.0  # meters
    driving_frequency: float = 5.0  # Hz (balanced for good stability)


@dataclass
class ParticleConfig:
    """Configuration of the simulated particle."""
    charge: float = 1.0  # Coulomb
    mass: float = 1.0  # kg


# Create instances
SIMULATION_CONFIG = SimulationConfig()
TRAP_CONFIG = TrapConfig()
PARTICLE_CONFIG = ParticleConfig() 