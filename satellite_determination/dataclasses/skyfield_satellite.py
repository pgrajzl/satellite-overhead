from skyfield.api import EarthSatellite, load
from dataclasses import dataclass
from enum import Enum
from typing import List



@dataclass
class SkyfieldSatellite:
    satellite: EarthSatellite
'''
@dataclass
class SkyfieldSatelliteList:
    satellites: List[EarthSatellite]

    @classmethod
    def load_tle(cls, tle_file) -> 'SkyfieldSatelliteList':
        return cls(
            satellites = load.tle_file(tle_file)
        )
'''