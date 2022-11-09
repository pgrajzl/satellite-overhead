from dataclasses import dataclass
from enum import Enum


class CoordinatesJsonKey(Enum):
    latitude = 'latitude'
    longitude = 'longitude'


@dataclass
class Coordinates:
    latitude: float
    longitude: float

    @classmethod
    def from_json(cls, info: dict) -> 'Coordinates':
        return Coordinates(
            latitude=info[CoordinatesJsonKey.latitude.value],
            longitude=info[CoordinatesJsonKey.longitude.value]
        )
