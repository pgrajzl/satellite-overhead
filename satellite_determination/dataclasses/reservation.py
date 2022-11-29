from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from satellite_determination.dataclasses.facility import Facility
from satellite_determination.dataclasses.time_window import TimeWindow


class ReservationJsonKey(Enum):
    facility = 'facility'
    time_start = 'time_start'
    time_end = 'time_end'


@dataclass
class Reservation:
    facility: Facility
    time: TimeWindow

    @classmethod
    def from_json(cls, info: dict) -> 'Reservation':
        return cls(
            facility=Facility.from_json(info[ReservationJsonKey.facility.value]),
            time=TimeWindow(begin=datetime.fromisoformat(info[ReservationJsonKey.time_start.value]),
                            end=datetime.fromisoformat(info[ReservationJsonKey.time_end.value]))
        )
