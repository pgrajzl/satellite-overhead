from typing import List

from sopp.custom_dataclasses.overhead_window import OverheadWindow
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.satellite.satellite import Satellite
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.event_finder.validator import Validator


class ValidatorSatellitesAreOverheadAtSpecificTimes(Validator):
    def __init__(self, overhead_times: List[TimeWindow]):
        self._overhead_times = overhead_times

    def get_overhead_windows(self, list_of_satellites: List[Satellite], reservation: Reservation) -> List[OverheadWindow]:
        return [OverheadWindow(satellite=satellite, overhead_time=overhead_time)
                for satellite, overhead_time in zip(list_of_satellites, self._overhead_times)
                if overhead_time.overlaps(reservation.time)]
