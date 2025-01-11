# constants.py

import numpy as np

# Physical constants
epsilon_0 = 8.854e-12  # Permittivity of free space (F/m)
lambda_amplitude = 1e-7  # Maximum linear charge density (C/m)
a = 0.1  # Distance of electrodes from origin (m)
omega = 2 * np.pi  # Angular frequency of oscillation (rad/s)

# Particle properties
q = 1e-10  # Charge of the particle (C)
m = 1e-6  # Mass of the particle (kg)
dt = 1e-2  # Time step for numerical integration (s)

# Grid
x = np.linspace(-0.1, 0.1, 10)
y = np.linspace(-0.1, 0.1, 10)
z = np.linspace(-0.1, 0.1, 9)
X, Y, Z = np.meshgrid(x, y, z)

# Electrode positions. Ignore the z axis, redundant here..
electrode_positions = np.array([
    [-a, 0, 0],   # Electrode at (-a, 0)
    [a, 0, 0],    # Electrode at (+a, 0)
    [0, -a, 0],   # Electrode at (0, -a)
    [0, a, 0],    # Electrode at (0, +a)
])