from dataclasses import dataclass
from functools import cached_property
from typing import List

from sopp.custom_dataclasses.overhead_window import OverheadWindow
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.satellite.satellite import Satellite
from sopp.event_finder.event_finder import EventFinder
from sopp.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesmill
from sopp.satellite_filters.filters import frequency_filter


@dataclass
class MainResults:
    satellites_above_horizon: List[OverheadWindow]
    interference_windows: List[OverheadWindow]


class Main:
    def __init__(self,
                 antenna_direction_path: List[PositionTime],
                 reservation: Reservation,
                 satellites: List[Satellite]):
        self._antenna_direction_path = antenna_direction_path
        self._reservation = reservation
        self._satellites = satellites

    def run(self) -> MainResults:
        overhead_windows_above_horizon = self._event_finder.get_satellites_above_horizon()

        satellites_above_horizon = []
        [
            satellites_above_horizon.append(window.satellite)
            for window in overhead_windows_above_horizon if window.satellite not in satellites_above_horizon
        ]

        event_finder = EventFinderRhodesmill(list_of_satellites=satellites_above_horizon,
                                             reservation=self._reservation,
                                             antenna_direction_path=self._antenna_direction_path)

        interference_windows = event_finder.get_satellites_crossing_main_beam()

        return MainResults(
            satellites_above_horizon=overhead_windows_above_horizon,
            interference_windows=interference_windows
        )

    @cached_property
    def _event_finder(self) -> EventFinder:
        return EventFinderRhodesmill(list_of_satellites=self._frequency_filtered_satellites,
                                     reservation=self._reservation,
                                     antenna_direction_path=self._antenna_direction_path)

    @property
    def _frequency_filtered_satellites(self) -> List[Satellite]:
        return list(filter(frequency_filter(self._reservation.frequency), self._satellites))
