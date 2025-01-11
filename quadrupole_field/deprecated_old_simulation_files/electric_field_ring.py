from manim import *
import numpy as np

import inspect

def debug_print(message=""):
    # Get the current frame
    frame = inspect.currentframe()
    # Get the caller frame
    caller_frame = frame.f_back
    # Extract information
    line_number = caller_frame.f_lineno
    function_name = caller_frame.f_code.co_name
    # Print the debug message
    print(f"[DEBUG] Line {line_number} in function '{function_name}': {message}")
    
class ElectricFieldRing3D(ThreeDScene):
    def construct(self):
        # Constants
        Q = 1e-6  # Total charge on the ring (Coulombs)
        R = 2     # Radius of the ring (arbitrary scale for visualization)
        epsilon_0 = 8.854187817e-12  # Permittivity of free space (F/m)

        # Ring parameters
        num_ring_points = 100
        theta = np.linspace(0, 2 * np.pi, num_ring_points)
        ring_points = np.array([R * np.cos(theta), R * np.sin(theta), np.zeros_like(theta)]).T

        # Grid for observation points
        grid_range = 3
        num_points = 7
        x = np.linspace(-grid_range, grid_range, num_points)
        y = np.linspace(-grid_range, grid_range, num_points)
        z = np.linspace(-grid_range, grid_range, num_points)
        observation_points = np.array(np.meshgrid(x, y, z)).reshape(3, -1).T

        # Electric field calculation
        def electric_field_at_point(obs_point):
            Ex, Ey, Ez = 0, 0, 0
            dq = Q / num_ring_points
            for point in ring_points:
                rx, ry, rz = obs_point - point
                r = np.sqrt(rx**2 + ry**2 + rz**2)
                # Skip if r is too small to avoid division by zero
                if r < 1e-12:  # Adjust the threshold as needed
                    continue

                dE = (1 / (4 * np.pi * epsilon_0)) * (dq / r**3) * np.array([rx, ry, rz])
                Ex += dE[0]
                Ey += dE[1]
                Ez += dE[2]
            return np.array([Ex, Ey, Ez])

        # Calculate fields
        field_vectors = [electric_field_at_point(p) for p in observation_points]
        normalized_vectors = [vec / np.linalg.norm(vec) if np.linalg.norm(vec) > 0 else vec for vec in field_vectors]

        # Create the ring
        ring = ParametricFunction(
            lambda t: np.array([R * np.cos(t), R * np.sin(t), 0]),
            t_range=np.array([0, 2 * np.pi]),
            color=BLUE
        )
        self.add(ring)

        # Create electric field vectors
        arrows = []
        for obs, vec in zip(observation_points, normalized_vectors):
            arrow = Arrow3D(
                start=obs,
                end=obs + vec * 0.5,  # Scale arrow length
                color=YELLOW,
                thickness=0.02
            )
            arrows.append(arrow)
        
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Create(ring))
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.05))

        # Add arrows
        for arrow in arrows:
            self.add(arrow)

        # Rotate scene
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.05)
        self.wait(10)