from abc import ABC

from .homework_02.exceptions import LowFuelError, NotEnoughFuel


class Vehicle(ABC):
    weight: int = 0
    started: bool = False
    fuel: float = 0
    fuel_consumption: float = 1

    def __init__(self, weight: int = 0, fuel: float = 0, fuel_consumption: float = 1) -> None:
        self.weight = weight
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption
        self.started = False

    def start(self) -> None:
        if not self.started:
            if self.fuel <= 0:
                raise LowFuelError()
            self.started = True

    def move(self, distance: float) -> None:
        required_fuel = distance * self.fuel_consumption
        if required_fuel > self.fuel:
            raise NotEnoughFuel()
        self.fuel -= required_fuel
