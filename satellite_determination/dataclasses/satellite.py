from dataclasses import dataclass
from enum import Enum
from os.path import realpath
from typing import Optional

from skyfield.sgp4lib import EarthSatellite

from satellite_determination.ListOfSatellites import loadSatellites
from satellite_determination.dataclasses.frequency_range import FrequencyRange
from satellite_determination.utilities import temporary_file


class SatelliteJsonKey(Enum):
    frequency = 'frequency'
    satellite_number = 'satellite_number'
    name = 'name'


@dataclass
class Satellite:
    argument_of_perigee: Optional[str] = None
    catalog_number: Optional[str] = None
    checksum: Optional[str] = None
    classification: Optional[str] = None
    eccentricity: Optional[str] = None
    element_set_number: Optional[str] = None
    ephemeris_type: Optional[str] = None
    epoch_day: Optional[str] = None
    epoch_year: Optional[str] = None
    frequency: Optional[FrequencyRange] = None
    inclination: Optional[str] = None
    international_designator_launch_number: Optional[str] = None
    international_designator_launch_piece: Optional[str] = None
    international_designator_year: Optional[str] = None
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
                    f'{self.catalog_number}{self.classification} '
                    f'{self.international_designator_year}{self.international_designator_launch_number}{self.international_designator_launch_piece: <3} '
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
