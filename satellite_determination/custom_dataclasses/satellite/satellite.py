from dataclasses import dataclass
from os.path import realpath
from pathlib import Path
from typing import List, Optional

from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite

from satellite_determination.custom_dataclasses.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.satellite.tle_information import TleInformation
from satellite_determination.utilities import temporary_file

NUMBER_OF_LINES_PER_TLE_OBJECT = 3


@dataclass
class Satellite:
    name: str
    tle_information: Optional[TleInformation] = None
    frequency: Optional[FrequencyRange] = None

    def to_rhodesmill(self) -> EarthSatellite:
        with temporary_file() as f:
            f.write(f'{self.name}\n')
            f.write('\n'.join(self.tle_information.to_tle_lines()))
            f.flush()
            return load.tle_file(url=realpath(f.name))[0]

    @classmethod
    def from_tle_file(cls, filepath: Path) -> List['Satellite']:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        name_line_indices = range(0, len(lines), NUMBER_OF_LINES_PER_TLE_OBJECT)
        return [Satellite(
            name=lines[name_line_index].strip(),
            tle_information=TleInformation.from_tle_lines(line1=lines[name_line_index + 1],
                                                          line2=lines[name_line_index + 2])
        ) for name_line_index in name_line_indices]