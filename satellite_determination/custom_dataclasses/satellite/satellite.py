from dataclasses import dataclass
from os.path import realpath
from typing import Optional

from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite

from satellite_determination.custom_dataclasses.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.satellite.tle_information import TleInformation
from satellite_determination.utilities import temporary_file


@dataclass
class Satellite:
    name: str
    tle_information: Optional[TleInformation] = None
    frequency: Optional[FrequencyRange] = None

    def to_rhodesmill(self) -> EarthSatellite:
        with temporary_file() as f:
            f.write(f'{self.name}\n')
            f.write(str(self.tle_information))
            f.flush()
            return load.tle_file(url=realpath(f.name))[0]
