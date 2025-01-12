# Paul Trap Experiment Data Analysis

Analysis of experimental measurements from a Paul trap setup, including particle charge and mass calculations, plus simulations of particle dynamics.

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

1. Install Poetry (dependency management):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Activate virtual environment:
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
jupyter notebook paultrap.ipynb
```

### Running Simulations

```bash
python -m quadrupole_field.main
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