from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.custom_dataclasses.frequency_range import FrequencyRange


class ReservationJsonKey(Enum):
    facility = 'facility'
    time_start = 'time_start'
    time_end = 'time_end'
    frequency = 'frequency'
    bandwidth = 'bandwidth'


@dataclass
class Reservation:
    facility: Facility
    time: TimeWindow
    frequency: FrequencyRange

    @classmethod
    def from_json(cls, info: dict) -> 'Reservation':
        return cls(
            facility=Facility.from_json(info[ReservationJsonKey.facility.value]),
            time=TimeWindow(begin=datetime.fromisoformat(info[ReservationJsonKey.time_start.value]),
                            end=datetime.fromisoformat(info[ReservationJsonKey.time_end.value])),
            frequency=FrequencyRange(frequency=info[ReservationJsonKey.frequency.value], bandwidth=info[ReservationJsonKey.bandwidth.value]) #TODO test this
        )
