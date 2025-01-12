"""Command line interface for the Paul trap simulation."""
import argparse

from argparse_pydantic import add_args_from_model, create_model_obj

from quadrupole_field.simulation.config import (
    OutputConfig,
    ParticleConfig,
    SimulationConfig,
    TrapConfig,
)


def parse_args() -> tuple[SimulationConfig, TrapConfig, ParticleConfig, OutputConfig]:
    """Parse command line arguments using Pydantic models."""
    parser = argparse.ArgumentParser(description="Paul Trap Simulation")
    
    # Add arguments from each Pydantic model with prefixes
    add_args_from_model(parser, SimulationConfig, "simulation")
    add_args_from_model(parser, TrapConfig, "trap")
    add_args_from_model(parser, ParticleConfig, "particle")
    add_args_from_model(parser, OutputConfig, "output")
    
    args = parser.parse_args()
    
    # Create model objects from parsed arguments (only takes model and args)
    sim_config = create_model_obj(SimulationConfig, args)
    trap_config = create_model_obj(TrapConfig, args)
    particle_config = create_model_obj(ParticleConfig, args)
    output_config = create_model_obj(OutputConfig, args)
    
    return sim_config, trap_config, particle_config, output_config 