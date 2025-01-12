"""Data structures for orbit parameters."""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class OrbitParameters:
    """Parameters describing a particle's orbit in the Paul trap."""

    voltage_amplitude: float
    driving_frequency: float
    initial_position: Tuple[float, float]
    initial_velocity: Tuple[float, float]
    stability_q: float
    secular_frequency: float
