from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.time_window import TimeWindow


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
