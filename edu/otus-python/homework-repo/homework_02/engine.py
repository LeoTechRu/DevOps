"""Module containing Engine dataclass."""

from dataclasses import dataclass


@dataclass
class Engine:
    volume: int
    pistons: int

