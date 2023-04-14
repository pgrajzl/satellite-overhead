from dataclasses import dataclass
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from typing import Optional


@dataclass
class Facility:
    point_coordinates: Coordinates
    name: str
    right_ascension: str
    declination: str
    beamwidth: Optional[float] = 3
    height: Optional[float] = 100 #TODO what is a good default?
