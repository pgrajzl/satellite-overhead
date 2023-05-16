from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.time_window import TimeWindow

'''
The Reservation class stores the Facility, as well as some additional reservation-specific information, such as reservation start and end times.
  + facility:   Facility object with RA facility and observation parameters
  + time:       TimeWindow that represents the start and end time of the ideal reservation.
  + frequency:  FrequencyRange of the requested observation. This is the frequency that the RA telescope wants to observe at.
'''

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
