"""Plane module with :class:`Plane` inheriting :class:`Vehicle`."""

from .base import Vehicle
from .exceptions import CargoOverload


class Plane(Vehicle):
    def __init__(self, weight: int, fuel: float, fuel_consumption: float, max_cargo: int) -> None:
        super().__init__(weight, fuel, fuel_consumption)
        self.max_cargo = max_cargo
        self.cargo = 0

    def load_cargo(self, cargo: int) -> None:
        if self.cargo + cargo > self.max_cargo:
            raise CargoOverload()
        self.cargo += cargo

    def remove_all_cargo(self) -> int:
        cargo = self.cargo
        self.cargo = 0
        return cargo

