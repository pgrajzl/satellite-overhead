from dataclasses import dataclass
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from typing import Optional


@dataclass
class Facility:
    point_coordinates: Coordinates
    name: str
    right_ascension: Optional[str] = None
    declination: Optional[str] = None
    beamwidth: Optional[float] = 3
    height: Optional[float] = 100 #TODO what is a good default?
    azimuth: Optional[float] = None #the azimuth and altitude parameters are only necessary if searching for satellites w/ stationary observation
    altitude: Optional[float] = 0 #default altitude to zero to find all sats above the horizon
