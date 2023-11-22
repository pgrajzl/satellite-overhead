from dataclasses import dataclass


@dataclass
class MeanMotion:
    first_derivative: float
    second_derivative: float
    value: float
