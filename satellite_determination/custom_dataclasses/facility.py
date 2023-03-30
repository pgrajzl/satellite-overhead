from dataclasses import dataclass
from satellite_determination.custom_dataclasses.coordinates import Coordinates


@dataclass
class Facility:
    point_coordinates: Coordinates
    name: str
    right_ascension: float
    declination: float
