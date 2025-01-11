# particle_dynamics.py

import numpy as np
from field_calculations import calculate_field_at_point
from constants import q, m, dt


def update_particle_position(particle_pos, particle_vel, electrodes, lambda_values):
    """
    Updates the position and velocity of a charged particle in the electric field.
    """
    # Compute the electric field at the particle's position
    E_particle = calculate_field_at_point(particle_pos, electrodes, lambda_values)
    # Update acceleration, velocity, and position
    particle_acc = (q / m) * E_particle
    particle_vel += particle_acc * dt
    particle_pos += particle_vel * dt
    return particle_pos, particle_vel
