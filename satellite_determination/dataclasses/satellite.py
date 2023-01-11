from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from os.path import realpath
from typing import Optional, Tuple

from skyfield.sgp4lib import EarthSatellite
from tletools import TLE

from satellite_determination.ListOfSatellites import loadSatellites
from satellite_determination.dataclasses.frequency_range import FrequencyRange
from satellite_determination.utilities import temporary_file


SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
SECONDS_PER_DAY = SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY

EPOCH_START_YEAR = 1970


class SatelliteJsonKey(Enum):
    frequency = 'frequency'
    satellite_number = 'satellite_number'
    name = 'name'

@dataclass
class InternationalDesignator:
    year: int
    launch_number: int
    launch_piece: str

    def __str__(self):
        return f'{str(self.year).zfill(2)}{str(self.launch_number).zfill(3)}{self.launch_piece: <3}'


@dataclass
class Satellite:
    argument_of_perigee: Optional[str] = None
    catalog_number: Optional[int] = None
    checksum: Optional[str] = None
    classification: Optional[str] = None
    eccentricity: Optional[str] = None
    element_set_number: Optional[str] = None
    ephemeris_type: Optional[str] = None
    timestamp: Optional[datetime] = None
    frequency: Optional[FrequencyRange] = None
    inclination: Optional[str] = None
    international_designator: Optional[InternationalDesignator] = None
    mean_anomaly: Optional[str] = None
    mean_motion: Optional[str] = None
    mean_motion_first_derivative: Optional[str] = None
    mean_motion_second_derivative: Optional[str] = None
    name: Optional[str] = None
    radiation_pressure_coefficient: Optional[str] = None
    revolution_number_at_epoch: Optional[str] = None
    right_ascension_of_descending_node: Optional[str] = None

    @classmethod
    def from_json(cls, info: dict) -> 'Satellite':
        return cls(
            frequency=FrequencyRange.from_json(info=info[SatelliteJsonKey.frequency.name]),
            catalog_number=info[SatelliteJsonKey.satellite_number.name],
            name=info[SatelliteJsonKey.name.name]
        )

    def to_rhodesmill(self) -> EarthSatellite:
        with temporary_file() as f:
            f.write(f'{self.name}')
            f.write(f'\n1 '
                    f'{str(self.catalog_number).zfill(5)}{self.classification.strip()} '
                    f'{str(self.international_designator_year).zfill(2)}{str(self.international_designator_launch_number).zfill(3)}{self.international_designator_launch_piece: <3} '
                    f'{self.epoch_year}{self.epoch_day} '
                    f'{self.mean_motion_first_derivative} '
                    f'{self.mean_motion_second_derivative: >8} '
                    f'{self.radiation_pressure_coefficient} '
                    f'{self.ephemeris_type} '
                    f'{self.element_set_number: >4}{self.checksum}')
            f.write(f'\n2 '
                    f'{self.catalog_number} '
                    f'{self.inclination: >8} '
                    f'{self.right_ascension_of_descending_node} '
                    f'{self.eccentricity} '
                    f'{self.argument_of_perigee} '
                    f'{self.mean_anomaly} '
                    f'{self.mean_motion}{self.revolution_number_at_epoch}{self.checksum}')
            f.flush()
            return loadSatellites(sat_tles=realpath(f.name))[0]

    def to_tle(self) -> Tuple[str, str, str]:
        # TLE(name=self.name,
        #     norad=self.catalog_number,
        #     classification=self.classification,
        #     int_desig=str(self.international_designator))

        name = (self.name or '').ljust(24)

        line1 = f'1 ' \
                f'{str(self.catalog_number or 0).zfill(5)}{(self.classification or "U").strip()}' \
                f' ' \
                f'{self.international_designator or " " * 8}' \
                f' ' \
                f'{str(self.timestamp.year - EPOCH_START_YEAR).zfill(2) if self.timestamp else "00"}' \
                f'{(str(self.timestamp.timetuple().tm_yday + (self.timestamp - datetime(self.timestamp.year, self.timestamp.month, self.timestamp.day)) / timedelta(days=1))[:12] if self.timestamp else "0.0").ljust(12, "0")}' \
                f' '

        line2 = f'2 ' \
                f'{str(self.catalog_number).zfill(5)}'

        return name, line1, line2
