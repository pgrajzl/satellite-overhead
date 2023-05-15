from astropy.coordinates import Angle
from dataclasses import dataclass
from datetime import datetime

'''
The ObservationPath class represents the telescope's position as a function of time by storing an altitude, azimuth, and timestamp. A telescope's
path across the sky as it tracks a celestial object is represented as a list of ObservationPaths.
  + altitude:   altitude of the telescope at time. Angle (type from Astropy).
  + azimuth:    azimuth of the telescope at time. Angle (from Astropy).
  + time:       time at which the telescope is at the stored altitude and azimuth. datetime.

'''

@dataclass
class ObservationPath:
    altitude: Angle
    azimuth: Angle
    time: datetime
