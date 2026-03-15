"""Car module implementing :class:`Car` that inherits :class:`Vehicle`."""

from .base import Vehicle
from .engine import Engine


class Car(Vehicle):
    def __init__(self, weight: int, fuel: float, fuel_consumption: float) -> None:
        super().__init__(weight, fuel, fuel_consumption)
        self.engine: Engine | None = None

    def set_engine(self, engine: Engine) -> None:
        self.engine = engine

