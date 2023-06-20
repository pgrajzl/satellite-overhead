from datetime import datetime
from typing import Iterable, List
from skyfield.api import load, wgs84
from skyfield.toposlib import GeographicPosition

from satellite_determination.azimuth_filter.azimuth_filtering import AzimuthFilter

from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder_rhodesmill.support.pseudo_continuous_timestamps_calculator import \
    PseudoContinuousTimestampsCalculator
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellites_within_main_beam_filter import AntennaPosition, \
    SatellitesWithinMainBeamFilter
from satellite_determination.event_finder.event_finder import EventFinder
from satellite_determination.event_finder.support.overhead_window_from_events import \
    EventRhodesmill, EventTypesRhodesmill, OverheadWindowFromEvents
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
    def get_overhead_windows(self):
        ts = load.timescale() #provides time objects with the data tables they need to translate between different time scales: the schedule of UTC leap seconds, and the value of ∆T over time.
        overhead_windows: List[OverheadWindow] = []
        time_start = ts.from_datetime(convert_datetime_to_utc(self._reservation.time.begin))
        time_end = ts.from_datetime(convert_datetime_to_utc(self._reservation.time.end))
        coordinates = self._facility_coordinates_rhodesmill
        for satellite in self._list_of_satellites:
            rhodesmill_earthsat = satellite.to_rhodesmill()
            event_times, events = rhodesmill_earthsat.find_events(coordinates, time_start, time_end, altitude_degrees=self._reservation.facility.elevation)
            if events.size != 0:
                rhodesmill_event_list = []
                for event_time, event in zip(event_times, events):
                    if event == 0:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.ENTERS, satellite=satellite, timestamp=event_time.utc_datetime())
                    elif event == 1:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.CULMINATES, satellite=satellite, timestamp=event_time.utc_datetime())
                    elif event == 2:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.EXITS, satellite=satellite, timestamp=event_time.utc_datetime())
                    rhodesmill_event_list.append(translated_event)
                sat_windows = OverheadWindowFromEvents(events=rhodesmill_event_list, reservation=self._reservation).get() #passes as custom dataclass Satellite
                for window in sat_windows:
                    overhead_windows.append(window)
        if self._reservation.facility.azimuth is not None:
            azimuth_filtered_windows = AzimuthFilter(overhead_windows=overhead_windows, reservation=self._reservation).filter_azimuth()
            return azimuth_filtered_windows
        else:
            return overhead_windows

    @property
    def _facility_coordinates_rhodesmill(self) -> GeographicPosition:
        return wgs84.latlon(
            latitude_degrees=self._reservation.facility.coordinates.latitude,
            longitude_degrees=self._reservation.facility.coordinates.longitude,
            elevation_m=self._reservation.facility.elevation)

    def get_overhead_windows_slew(self) -> List[OverheadWindow]:
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
