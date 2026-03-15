"""
Объявите следующие исключения:
- LowFuelError
- NotEnoughFuel
- CargoOverload
"""


class LowFuelError(Exception):
    """Raised when starting the vehicle with zero fuel."""


class NotEnoughFuel(Exception):
    """Raised when there is not enough fuel to move the required distance."""


class CargoOverload(Exception):
    """Raised when attempting to load cargo that exceeds the maximum capacity."""

