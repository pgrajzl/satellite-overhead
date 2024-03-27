from functools import cached_property
from typing import List, Type
from datetime import timedelta

from sopp.event_finder.event_finder import EventFinder
from sopp.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesmill
from sopp.custom_dataclasses.configuration import Configuration
from sopp.custom_dataclasses.overhead_window import OverheadWindow
from sopp.custom_dataclasses.satellite.satellite import Satellite
from sopp.custom_dataclasses.runtime_settings import RuntimeSettings
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.custom_dataclasses.time_window import TimeWindow


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
        self._validate_antenna_direction_path()
        return self._event_finder.get_satellites_crossing_main_beam()

    @cached_property
    def _event_finder(self) -> EventFinder:
        return self._event_finder_class(
            list_of_satellites=self._validated_configuration.satellites,
            reservation=self._validated_configuration.reservation,
            antenna_direction_path=self._validated_configuration.antenna_direction_path,
            runtime_settings=self._validated_configuration.runtime_settings,
        )

    @cached_property
    def _validated_configuration(self)-> Configuration:
        self._validate_satellites()
        self._validate_runtime_settings()
        self._validate_reservation()

        return self._configuration

    def _validate_satellites(self):
        satellites = self._configuration.satellites
        if not satellites:
            raise ValueError('Satellites list empty.')
        if not isinstance(satellites, list):
            raise TypeError('Satellites must be a list.')
        if not all(isinstance(item, Satellite) for item in satellites):
            raise TypeError('All elements in satellites must be of type Satellite.')

    def _validate_runtime_settings(self):
        runtime_settings = self._configuration.runtime_settings
        if not isinstance(runtime_settings, RuntimeSettings):
            raise TypeError('runtime_settings must be of type RuntimeSettings.')
        if not isinstance(runtime_settings.time_continuity_resolution, timedelta):
            raise TypeError('time_continuity_resolution must be of type timedelta.')
        if not isinstance(runtime_settings.concurrency_level, int):
            raise TypeError('concurrency_level must be an integer.')

        if runtime_settings.time_continuity_resolution < timedelta(seconds=1):
            raise ValueError('time_continuity_resolution must be at least 1 second.')
        if runtime_settings.concurrency_level < 1:
            raise ValueError('concurrency_level must be at least 1.')
        if runtime_settings.min_altitude < 0.0:
            raise ValueError('min_altitude must be non-negative.')

    def _validate_reservation(self):
        reservation = self._configuration.reservation
        if not isinstance(reservation, Reservation):
            raise TypeError('reservation must be of type Reservation.')
        if not isinstance(reservation.time, TimeWindow):
            raise TypeError('reservation.time must be of type TimeWindow.')

        if reservation.time.begin >= reservation.time.end:
            raise ValueError('reservation.time.begin time is later than or equal to end time.')
        if reservation.facility.beamwidth <= 0:
            raise ValueError('reservation.facility.beamwidth must be greater than 0.')

    def _validate_antenna_direction_path(self):
        antenna_direction_path = self._configuration.antenna_direction_path
        if not antenna_direction_path:
            raise ValueError('No antenna direction path provided.')
        if not isinstance(antenna_direction_path, list):
            raise TypeError('Antenna direction path must be a list.')
        if not all(isinstance(item, PositionTime) for item in antenna_direction_path):
            raise TypeError('All elements in antenna direction path must be of type PositionTime.')

        for current_time, next_time in zip(antenna_direction_path, antenna_direction_path[1:]):
            if current_time.time >= next_time.time:
                raise ValueError('Times in antenna_direction_path must be increasing.')
