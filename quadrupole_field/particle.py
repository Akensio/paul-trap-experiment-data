import numpy as np


class Particle:
    def __init__(self, charge, mass, position, velocity):
        """
        Initialize the particle with its properties.
        :param charge: Charge of the particle.
        :param mass: Mass of the particle.
        :param position: Initial position as a tuple (x, y).
        :param velocity: Initial velocity as a tuple (vx, vy).
        """
        self.q = charge
        self.m = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

    def update(self, electric_field, dt):
        """
        Update the particle's position and velocity.
        :param electric_field: Electric field vector (Ex, Ey).
        :param dt: Time step.
        """
        Ex, Ey = electric_field
        acceleration = self.q * np.array([Ex, Ey]) / self.m
        self.velocity += acceleration * dt
        self.position += self.velocity * dt