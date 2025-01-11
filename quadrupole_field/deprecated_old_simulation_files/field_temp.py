import numpy as np
import matplotlib.pyplot as plt

def electric_field_ring(Q, R, observation_points, num_points=1000):
    """
    Calculate the electric field due to a ring of charge at given observation points in 3D space.

    Parameters:
    Q (float): Total charge on the ring (Coulombs).
    R (float): Radius of the ring (meters).
    observation_points (ndarray): Array of points (x, y, z) where the electric field is calculated.
    num_points (int): Number of discrete points to approximate the ring.

    Returns:
    ndarray: Electric field vectors at the observation points.
    """
    # Constants
    epsilon_0 = 8.854187817e-12  # Permittivity of free space (F/m)

    # Discretize the ring
    theta = np.linspace(0, 2 * np.pi, num_points)
    x_ring = R * np.cos(theta)
    y_ring = R * np.sin(theta)
    z_ring = np.zeros_like(theta)

    # Charge element (dq = Q / num_points)
    dq = Q / num_points

    # Initialize electric field array
    E = np.zeros_like(observation_points)

    # Loop over all observation points
    for i, point in enumerate(observation_points):
        x_obs, y_obs, z_obs = point
        Ex, Ey, Ez = 0.0, 0.0, 0.0

        # Calculate the electric field contribution from each charge element
        for x, y, z in zip(x_ring, y_ring, z_ring):
            # Distance vector from ring element to observation point
            rx = x_obs - x
            ry = y_obs - y
            rz = z_obs - z
            r = np.sqrt(rx**2 + ry**2 + rz**2)

            # Electric field contribution (Coulomb's Law)
            dE = (1 / (4 * np.pi * epsilon_0)) * (dq / r**3) * np.array([rx, ry, rz])

            # Add to the total electric field
            Ex += dE[0]
            Ey += dE[1]
            Ez += dE[2]

        # Store the total electric field
        E[i] = np.array([Ex, Ey, Ez])

    return E

# Parameters
Q = 1e-6  # Total charge on the ring (Coulombs)
R = 0.1   # Radius of the ring (meters)

# Generate a grid of observation points
x = np.linspace(-0.2, 0.2, 20)
y = np.linspace(-0.2, 0.2, 20)
z = np.linspace(-0.2, 0.2, 20)
X, Y, Z = np.meshgrid(x, y, z)
observation_points = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

# Calculate the electric field
E = electric_field_ring(Q, R, observation_points)

# Reshape for visualization
Ex, Ey, Ez = E[:, 0].reshape(X.shape), E[:, 1].reshape(X.shape), E[:, 2].reshape(X.shape)

# Plot the electric field using quiver
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, Ex, Ey, Ez, length=0.01, normalize=True)
ax.set_title("Electric Field of a Ring of Charge")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
plt.show()