from astropy.coordinates import Angle
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PositionTime:
    altitude: Angle
    azimuth: Angle
    time: datetime

