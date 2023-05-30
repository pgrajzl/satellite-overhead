from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from math import isclose
from typing import List

from skyfield.toposlib import GeographicPosition, wgs84

from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.utilities import convert_datetime_to_utc


@dataclass
class SatellitePosition:
    satellite_positions_with_respect_to_facility: List[PositionTime]
    antenna_direction: PositionTime


@dataclass
class EnterAndExitEvents:
    enter: List[datetime]
    exit: List[datetime]


class OverheadWindowSlew:
    def __init__(self,
                 facility: Facility,
                 satellite_positions: List[SatellitePosition]):
        self._facility = facility
        self._satellite_positions = satellite_positions
        self._previously_in_view = False

    def run(self) -> List[TimeWindow]:
        events = self._get_enter_and_exit_events()
        return [TimeWindow(begin=begin_event, end=exit_event) for begin_event, exit_event in zip(events.enter, events.exit)]

    def _get_enter_and_exit_events(self) -> EnterAndExitEvents:
        enter_events = []
        exit_events = []
        for position in self._satellite_positions_by_antenna_time:
            for satellite_position in self._sort_satellite_positions_by_time(position.satellite_positions_with_respect_to_facility):
                azimuth_satellite = min(satellite_position.azimuth, 360 - satellite_position.azimuth)
                azimuth_facility = min(position.antenna_direction.azimuth, 360 - position.antenna_direction.azimuth)
                is_within_beamwidth_altitude = isclose(satellite_position.altitude,
                                                       position.antenna_direction.altitude,
                                                       abs_tol=self._half_beamwidth)
                is_within_beamwidth_azimuth = isclose(azimuth_satellite, azimuth_facility, abs_tol=self._half_beamwidth)
                now_in_view = is_within_beamwidth_altitude and is_within_beamwidth_azimuth
                if now_in_view and not self._previously_in_view:
                    enter_events.append(convert_datetime_to_utc(position.time))
                    self._previously_in_view = True
                elif not now_in_view and self._previously_in_view:
                    exit_events.append(convert_datetime_to_utc(position.time))
                    self._previously_in_view = False
        exit_events.append(self._last_time)
        return EnterAndExitEvents(enter=enter_events, exit=exit_events)

    @property
    def _last_time(self) -> datetime:
        satellite_positions_at_last_antenna_time = self._satellite_positions_by_antenna_time[-1].satellite_positions_with_respect_to_facility
        return self._sort_satellite_positions_by_time(satellite_positions=satellite_positions_at_last_antenna_time)[-1].time

    @staticmethod
    def _sort_satellite_positions_by_time(satellite_positions: List[PositionTime]) -> List[PositionTime]:
        return sorted(satellite_positions, key=lambda x: x.time)

    @cached_property
    def _satellite_positions_by_antenna_time(self) -> List[SatellitePosition]:
        return sorted(self._satellite_positions, key=lambda x: x.antenna_direction.time)

    @cached_property
    def _coordinates(self) -> GeographicPosition:
        return wgs84.latlon(self._facility.point_coordinates.latitude,
                            self._facility.point_coordinates.longitude)
    
    @cached_property
    def _half_beamwidth(self) -> float:
        return self._facility.beamwidth / 2
