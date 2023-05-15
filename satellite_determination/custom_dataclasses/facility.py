from dataclasses import dataclass
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from typing import Optional

'''
The Facility data class contains the observation parameters of the facility and the object it is tracking, including coordinates 
of the RA telescope and its beamwidth, as well as the right ascension and declination values for its observation target. A description
of each of the values is below:

-point_coordinates: latitude and longitude of RA facility. From custom data class Coordinates in custom_dataclasses/coordinates.py
-name:              (optional) name of the facility. String.
-right_ascension:   (optional) the right ascension of the observation target. This is not needed if you are 
                    performing an observation in a stationary position and the telescope will not slew. String.
-declination:       (optional) the declination of the observation target. This is not needed if you are performing 
                    an observation in a stationary position and the telescope will not slew. String.
-beamwidth:         (optional) beamwidth of the telescope. This is optional and will assign a default value of 3 
                    if left unassigned. float.
-height:            (optional) height of the telescope. float.
-azimuth:           (optional) azimuth of the telescope. Only used if performing an observation in a stationary position
                    so not often needed. float.
-elevation:         (optional) elevation (altitude) of the telescope. Only used if performing an observation in a stationary 
                    position so not often needed. float.
                    
Many of the parameters are left optional as what is needed varies depending on which function of SOPP you are trying to use. If finding interference
as an RA telescope tracks a target across the sky, the RA and Dec of the target is necessary but not the azimuth and elevation. The opposite is true
for stationary observations.

'''

@dataclass
class Facility:
    point_coordinates: Coordinates
    name: Optional[str] = 'Unnamed Facility'
    right_ascension: Optional[str] = None
    declination: Optional[str] = None
    beamwidth: Optional[float] = 3
    height: Optional[float] = 100 #TODO what is a good default?
    azimuth: Optional[float] = None #the azimuth and altitude parameters are only necessary if searching for satellites w/ stationary observation
    elevation: Optional[float] = 0 #default altitude to zero to find all sats above the horizon
