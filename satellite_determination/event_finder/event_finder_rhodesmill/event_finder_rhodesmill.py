from dataclasses import replace
from datetime import datetime
from typing import Iterable, List

from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder_rhodesmill.support.pseudo_continuous_timestamps_calculator import \
    PseudoContinuousTimestampsCalculator
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellites_within_main_beam_filter import AntennaPosition, \
    SatellitesWithinMainBeamFilter
from satellite_determination.event_finder.event_finder import EventFinder
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.utilities import convert_datetime_to_utc


class EventFinderRhodesMill(EventFinder):
    '''
    The EventFinderRhodesMill is the module that determines if a satellite interferes with an RA observation. It has three functions:

      + get_overhead_windows_slew():    determines if a satellite crosses the telescope's main beam as the telescope moves across the sky
                                        by looking for intersections of azimuth and altitude and returning a list of OverheadWindows for
                                        events where this occurs
      + get_overhead_windows():         Determines the satellites visible above the horizon during the search window and returns a list of
                                        OverheadWindows for each event. This can be used to find all satellite visible over the horizon or
                                        to determine events for a stationary observation if an azimuth and altitude is provided

    '''
    def get_satellites_above_horizon(self):
        facility_with_beam_width_that_sees_entire_sky = replace(self._reservation.facility, beamwidth=360)
        event_finder = EventFinderRhodesMill(list_of_satellites=self._list_of_satellites,
                                             reservation=replace(self._reservation, facility=facility_with_beam_width_that_sees_entire_sky),
                                             antenna_direction_path=[PositionTime(altitude=90, azimuth=0, time=self._reservation.time.begin)])
        return event_finder.get_satellites_crossing_main_beam()

    def get_satellites_crossing_main_beam(self) -> List[OverheadWindow]:
        return [
            overhead_window
            for satellite in self._list_of_satellites
            for overhead_window in self._get_satellite_overhead_windows(satellite=satellite)
        ]

    def _get_satellite_overhead_windows(self, satellite: Satellite) -> Iterable[OverheadWindow]:
        antenna_direction_end_times = [antenna_direction.time for antenna_direction in self._antenna_direction_path[1:]] \
                                      + [self._reservation.time.end]
        antenna_positions = [
            AntennaPosition(
                satellite_positions=self._get_satellite_positions(
                    satellite=satellite,
                    time_window=TimeWindow(
                        begin=max(self._reservation.time.begin, antenna_direction.time),
                        end=end_time
                    )),
                antenna_direction=antenna_direction)
            for antenna_direction, end_time in zip(self._antenna_direction_path, antenna_direction_end_times)
            if end_time > self._reservation.time.begin]
        time_windows = SatellitesWithinMainBeamFilter(facility=self._reservation.facility,
                                                      antenna_positions=antenna_positions,
                                                      cutoff_time=self._reservation.time.end).run()
        return (OverheadWindow(satellite=satellite, overhead_time=time_window) for time_window in time_windows)

    def _get_satellite_positions(self, satellite: Satellite, time_window: TimeWindow) -> List[PositionTime]:
        pseudo_continuous_timestamps = PseudoContinuousTimestampsCalculator(time_window=time_window,
                                                                            resolution=self._time_continuity_resolution).run()
        return [self._get_position_with_respect_to_facility(satellite=satellite,
                                                            timestamp=convert_datetime_to_utc(timestamp),
                                                            facility=self._reservation.facility)
                for timestamp in pseudo_continuous_timestamps]

    def _get_position_with_respect_to_facility(self,
                                               satellite: Satellite,
                                               timestamp: datetime,
                                               facility: Facility) -> PositionTime:
        return self._satellite_position_with_respect_to_facility_retriever_class(satellite=satellite,
                                                                                 timestamp=timestamp,
                                                                                 facility=facility).run()
