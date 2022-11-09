from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from satellite_determination.dataclasses.facility import Facility


class ReservationJsonKey(Enum):
    facility = 'facility'
    time_start = 'time_start'
    time_end = 'time_end'


@dataclass
class Reservation:
    facility: Facility
    time_start: datetime
    time_end: datetime

    @classmethod
    def from_json(cls, info: dict) -> 'Reservation':
        return cls(
            facility=Facility.from_json(info[ReservationJsonKey.facility.value]),
            time_start=datetime.fromisoformat(info[ReservationJsonKey.time_start.value]),
            time_end=datetime.fromisoformat(info[ReservationJsonKey.time_end.value])
        )
