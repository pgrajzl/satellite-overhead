from astropy.coordinates import Angle
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ObservationPath:
    altitude: Angle
    azimuth: Angle
    time: datetime

    @classmethod
    def astropy_ang_to_float(cls, angle: Angle):
        return float(angle)

