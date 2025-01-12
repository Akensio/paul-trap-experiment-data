"""Configuration settings for the Paul trap simulation using Pydantic.
This module contains all configurable parameters for the simulation, organized into
logical groups. Each parameter can be adjusted to explore different trap behaviors.
"""


from pydantic import BaseModel, Field


class SimulationConfig(BaseModel):
    """Time-related configuration for the simulation.
    
    Controls the temporal resolution and duration of the simulation. Smaller dt values
    provide more accurate results but increase computation time.
    """
    dt: float = Field(
        default=0.001,
        description="Time step size in seconds",
        gt=0
    )
    total_time: float = Field(
        default=5.0,
        description="Total simulation duration in seconds",
        gt=0
    )


class TrapConfig(BaseModel):
    """Physical configuration of the trap system.
    
    Defines the fundamental trap parameters that determine its operation.
    The rod_distance and driving_frequency are key parameters that affect
    particle stability.
    """
    rod_distance: float = Field(
        default=1.0,
        description="Distance from center to rods in meters",
        gt=0
    )
    driving_frequency: float = Field(
        default=5.0,
        description="RF frequency in Hz",
        gt=0
    )


class ParticleConfig(BaseModel):
    """Configuration of the simulated particle.
    
    Defines the physical properties of the trapped particle. These values
    determine the particle's response to the electric field and its
    stability characteristics.
    """
    charge: float = Field(
        default=1.0,
        description="Particle charge in Coulombs"
    )
    mass: float = Field(
        default=1.0,
        description="Particle mass in kilograms",
        gt=0
    )


class OutputConfig(BaseModel):
    """Configuration for simulation output and visualization."""
    save_video: bool = Field(
        default=False,
        description="Save animation as video file"
    )
    output_file: str = Field(
        default="paul_trap_simulation.mp4",
        description="Output video filename"
    )


# Default configurations
DEFAULT_SIMULATION_CONFIG = SimulationConfig()
DEFAULT_TRAP_CONFIG = TrapConfig()
DEFAULT_PARTICLE_CONFIG = ParticleConfig()
DEFAULT_OUTPUT_CONFIG = OutputConfig()
