from dataclasses import dataclass
from enum import Enum
from typing import Optional

from satellite_determination.custom_dataclasses.coordinates import Coordinates


class FacilityJsonKey(Enum):
    elevation = 'elevation'
    name = 'name'
    point_coordinates = 'point_coordinates'
    azimuth = 'azimuth'


@dataclass
class Facility:
    elevation: float
    point_coordinates: Coordinates
    azimuth: float
    name: str
    beamwidth: Optional[float] = 3

    @classmethod
    def from_json(cls, info: dict) -> 'Facility':
        return cls(
            elevation=info[FacilityJsonKey.elevation.value],
            point_coordinates=Coordinates.from_json(info[FacilityJsonKey.point_coordinates.value]),
            name=info[FacilityJsonKey.name.value],
            azimuth=info[FacilityJsonKey.azimuth.value]
        )
