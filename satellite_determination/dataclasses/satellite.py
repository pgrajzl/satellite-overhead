from dataclasses import dataclass
from enum import Enum

from satellite_determination.dataclasses.frequency_range import FrequencyRange


class SatelliteJsonKey(Enum):
    frequency = 'frequency'
    satellite_number = 'satellite_number'
    name = 'name'


@dataclass
class Satellite:
    frequency: FrequencyRange
    satellite_number: str
    name: str

    @classmethod
    def from_json(cls, info: dict) -> 'Satellite':
        return cls(
            frequency=FrequencyRange.from_json(info=info[SatelliteJsonKey.frequency.name]),
            satellite_number=info[SatelliteJsonKey.satellite_number.name],
            name=info[SatelliteJsonKey.name.name]
        )
