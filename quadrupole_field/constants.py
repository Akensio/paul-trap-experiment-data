"""Physical constants and fundamental parameters for the quadrupole trap simulation."""

# Physical constants
ELEMENTARY_CHARGE: float = 1.602176634e-19  # Coulomb
ELECTRON_MASS: float = 9.1093837015e-31    # kg
PROTON_MASS: float = 1.67262192369e-27     # kg

# Trap parameters
ROD_DISTANCE: float = 1.0                   # meters
VOLTAGE_AMPLITUDE: float = 10.0             # volts
DRIVING_FREQUENCY: float = 1.0              # Hz

# Particle parameters
PARTICLE_CHARGE: float = ELEMENTARY_CHARGE  # Coulomb
PARTICLE_MASS: float = ELECTRON_MASS       # kg
INITIAL_POSITION: tuple[float, float] = (0.1, 0.1)  # meters
INITIAL_VELOCITY: tuple[float, float] = (0.0, 0.0)  # meters/second