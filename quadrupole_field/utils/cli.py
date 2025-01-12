"""Command line interface for the Paul trap simulation."""
import argparse

from argparse_pydantic import add_args_from_model, create_model_obj

from quadrupole_field.simulation.config import (
    InitialConditionsConfig,
    OutputConfig,
    ParticleConfig,
    SimulationConfig,
    TrapConfig,
)


def parse_args() -> tuple[
    SimulationConfig, TrapConfig, ParticleConfig, OutputConfig, InitialConditionsConfig
]:
    """Parse command line arguments using Pydantic models."""
    parser = argparse.ArgumentParser(description="Paul Trap Simulation")
    
    # Add arguments from each Pydantic model with prefixes
    add_args_from_model(parser, SimulationConfig, create_group=True)
    add_args_from_model(parser, TrapConfig, create_group=True)
    add_args_from_model(parser, ParticleConfig, create_group=True)
    add_args_from_model(parser, OutputConfig, create_group=True)
    add_args_from_model(parser, InitialConditionsConfig, create_group=True)
    
    args = parser.parse_args()
    
    # Create model objects from parsed arguments
    sim_config = create_model_obj(SimulationConfig, args)
    trap_config = create_model_obj(TrapConfig, args)
    particle_config = create_model_obj(ParticleConfig, args)
    output_config = create_model_obj(OutputConfig, args)
    initial_config = create_model_obj(InitialConditionsConfig, args)
    
    return sim_config, trap_config, particle_config, output_config, initial_config 