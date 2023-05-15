from dataclasses import dataclass, field
from os.path import realpath
from pathlib import Path
from typing import List, Optional

from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite

from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.satellite.tle_information import TleInformation
from satellite_determination.utilities import temporary_file

'''
The Satellite data class stores all of the TLE information for each satellite, which is loaded from a TLE file using the class method from_tle_file()
and can be converted to a Skyfield API object EarthSatellite using the to_rhodesmill() method. It also stores all the frequency information
for each satellite.

  + name:               name of satellite. string.
  + tle_information:    stores TLE information. TleInformation is another custom object to store TLE data and can be found in
                        ROOT/satellite_determination/custom_dataclasses/satellite/tle_information.py
  + frequency:          list of type FrequencyRange. FrequencyRange is a custom dataclass that stores a center frequency and bandwidth.
  

  + to_rhodesmill():    class method to convert a Satellite object into a Rhodemill-Skyfield EarthSatellite object for use with the Skyfield API
  + from_tle_file():    class method to load Satellite from provided TLE file. Returns a list of type Satellite.
'''

NUMBER_OF_LINES_PER_TLE_OBJECT = 3


@dataclass
class Satellite:
    name: str
    tle_information: Optional[TleInformation] = None
    frequency: List[FrequencyRange] = field(default_factory=list)

    def to_rhodesmill(self) -> EarthSatellite:
        with temporary_file() as f:
            f.write(f'{self.name}\n')
            f.write('\n'.join(self.tle_information.to_tle_lines()))
            f.flush()
            return load.tle_file(url=realpath(f.name))[0]

    @classmethod
    def from_tle_file(cls, tlefilepath: Path) -> List['Satellite']:
        with open(tlefilepath, 'r') as f:
            lines = f.readlines()
        name_line_indices = range(0, len(lines), NUMBER_OF_LINES_PER_TLE_OBJECT)
        return [Satellite(
            name=lines[name_line_index].strip(),
            tle_information=TleInformation.from_tle_lines(line1=lines[name_line_index + 1],
                                                          line2=lines[name_line_index + 2])
        ) for name_line_index in name_line_indices]
