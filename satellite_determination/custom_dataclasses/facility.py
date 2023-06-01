from dataclasses import dataclass
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from typing import Optional


@dataclass
class Facility:
    '''
    The Facility data class contains the observation parameters of the facility and the object it is tracking, including coordinates
    of the RA telescope and its beamwidth, as well as the right ascension and declination values for its observation target:

    -point_coordinates: location of RA facility. Coordinates.
    -beamwidth:         beamwidth of the telescope. float. Defaults to 3
    -height:            height of the telescope. float. Defaults to 100
    -name:              name of the facility. String. Defaults to 'Unnamed Facility'
    -elevation:         elevation (altitude) of the telescope. float. Defaults to 0 to find all sats above the horizon
    -right_ascension:   (optional) the right ascension of the observation target. String.
    -declination:       (optional) the declination of the observation target. String.
    -azimuth:           (optional) azimuth of the telescope. float.

    If finding interference as an RA telescope tracks a target across the sky, the right ascension and declination of
    the target is necessary but not the azimuth and elevation. The opposite is true for stationary observations.

    '''
    point_coordinates: Coordinates
    beamwidth: float = 3
    height: float = 100
    name: Optional[str] = 'Unnamed Facility'
    elevation: float = 0
    right_ascension: Optional[str] = None
    declination: Optional[str] = None
    azimuth: Optional[float] = None


    @property
    def half_beamwidth(self) -> float:
        return self.beamwidth / 2
