# Paul Trap Experiment Data Analysis

Analysis of experimental measurements from a Paul trap setup, including particle charge and mass calculations, plus simulations of particle dynamics. The simulations don't really work, but they're a good educational project.

## Overview

This repository contains:
1. Analysis of real Paul trap experimental data
2. Simulation of particle dynamics in a Paul trap
3. Visualization tools for both experimental and simulation results

## Repository Structure
```
paul_trap_experiment_data_analysis/
├── paultrap.ipynb # Experimental data analysis
├── data.xlsx # Raw experimental measurements
├── ODR/ # Orthogonal Distance Regression utilities
│ └── ...
├── quadrupole_field/ # Simulation package
│ ├── core/ # Core physics implementations
│ ├── simulation/ # Simulation logic
│ ├── utils/ # Utility functions
│ └── visualization/ # Visualization components
└── README.md
```

## Setup and Installation

1. Ensure you have Python 3.12+ installed

2. Install Poetry (dependency management):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:
```bash
poetry install
```

4. Activate virtual environment:
```bash
poetry shell
```


## Features

### 1. Experimental Analysis
- Pixel-to-millimeter calibration
- Particle diameter and mass calculations
- Charge-to-mass ratio determination
- Trajectory analysis

### 2. Particle Simulation
The simulation models a Paul trap with:
- Quadrupole electric field calculations
- Particle dynamics using symplectic integration
- Configurable trap parameters
- Real-time visualization

## Usage

### Experimental Analysis

```bash
cd paul_trap_experiment_data_analysis
jupyter notebook paultrap.ipynb
```

### Running Simulations

Basic usage:
```bash
python -m quadrupole_field.main
```

With custom trap and particle parameters:
```bash
python -m quadrupole_field.main \
--simulation.dt 0.0005 \
--simulation.total_time 10.0 \
--trap.rod_distance 0.5 \
--trap.driving_frequency 10.0 \
--particle.charge 1e-6 \
--particle.mass 1e-9 \
--output.save_video \
--output.output_file "custom_simulation.mp4"
```

With manual override of initial conditions:
```bash
python -m quadrupole_field.main \
--initial.voltage_amplitude 1000 \
--initial.initial_position 0.001,0 \
--initial.initial_velocity 0,0.1
```

Available parameters:
- Simulation settings:
  - `--dt`: Time step size in seconds (default: 0.001)
  - `--total_time`: Total simulation duration in seconds (default: 5.0)
- Trap configuration:
  - `--rod_distance`: Distance from center to rods in meters (default: 1.0)
  - `--driving_frequency`: RF frequency in Hz (default: 5.0)
- Particle properties:
  - `--charge`: Particle charge in Coulombs (default: 1.0)
  - `--mass`: Particle mass in kilograms (default: 1.0)
- Initial conditions (optional overrides):
  - `--voltage_amplitude`: Manual override for voltage amplitude in Volts
  - `--initial_position_x`: Manual override for initial x position in meters. Must be overridden alongside y.
  - `--initial_position_y`: Manual override for initial y position in meters. Must be overridden alongside x.
  - `--initial_velocity_x`: Manual override for initial velocity Vx in m/s. Must be overridden alongside Vy.
  - `--initial_velocity_y`: Manual override for initial velocity Vy in m/s. Must be overridden alongside Vx.
- Output options:
  - `--save_video`: Save animation to file (boolean)
  - `--output_file`: Output video filename (default: "paul_trap_simulation.mp4")

Note: Initial conditions are automatically calculated for stable orbits if not manually specified.

To see all available options:
```bash
python -m quadrupole_field.main --help
```

## Configuration

### Simulation Parameters
The simulation can be configured through dataclasses in `quadrupole_field/simulation/config.py`:
- `SimulationConfig`: Time steps and duration
- `TrapConfig`: Physical trap parameters
- `ParticleConfig`: Particle properties

### Visualization Settings
Visualization parameters can be adjusted in `quadrupole_field/visualization/config.py`:
- Plot dimensions and styling
- Animation parameters
- Field visualization settings

## Requirements

See `pyproject.toml` for full dependencies. Key requirements:
- Python 3.12+
- pandas
- numpy
- matplotlib
- scipy
- plotly
- dash (for interactive visualizations)
- gradio (for UI components)

## Development

1. Code formatting:
```bash
poetry run black .
poetry run isort .
```

2. Running tests (TODO)

## Authors

- Eitan S
- Gadi B

## License

MIT License