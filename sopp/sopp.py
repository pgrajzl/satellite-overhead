from functools import cached_property
from typing import List, Type

from sopp.event_finder.event_finder import EventFinder
from sopp.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesmill
from sopp.custom_dataclasses.configuration import Configuration
from sopp.custom_dataclasses.overhead_window import OverheadWindow


class Sopp:
    def __init__(
        self,
        configuration: Configuration,
        event_finder_class: Type[EventFinder] = EventFinderRhodesmill
    ):
        self._configuration = configuration
        self._event_finder_class = event_finder_class

    def get_satellites_above_horizon(self) -> List[OverheadWindow]:
        return self._event_finder.get_satellites_above_horizon()

    def get_satellites_crossing_main_beam(self) -> List[OverheadWindow]:
        return self._event_finder.get_satellites_crossing_main_beam()

    @cached_property
    def _event_finder(self) -> EventFinder:
        return self._event_finder_class(
            list_of_satellites=self._configuration.satellites,
            reservation=self._configuration.reservation,
            antenna_direction_path=self._configuration.antenna_direction_path,
            runtime_settings=self._configuration.runtime_settings,
        )
