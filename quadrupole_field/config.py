"""Configuration settings for simulation."""

from dataclasses import dataclass


@dataclass
class SimulationConfig:
    dt: float = 0.001
    total_time: float = 5.0


# Create instance
SIMULATION_CONFIG = SimulationConfig()
