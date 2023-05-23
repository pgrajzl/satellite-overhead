from datetime import timedelta
from typing import List
from skyfield.api import load, wgs84
from satellite_determination.azimuth_filter.azimuth_filtering import AzimuthFilter
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder import EventFinder
from satellite_determination.event_finder.support.overhead_window_from_events import \
    EventRhodesmill, EventTypesRhodesmill, OverheadWindowFromEvents
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
        coordinates = wgs84.latlon(self._reservation.facility.point_coordinates.latitude, self._reservation.facility.point_coordinates.longitude)
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

    def get_overhead_windows_slew(self):
        ts = load.timescale()
        azimuth_filtered_overhead_windows = []
        coordinates = wgs84.latlon(self._reservation.facility.point_coordinates.latitude,
                                   self._reservation.facility.point_coordinates.longitude)
        half_beamwidth = self._reservation.facility.beamwidth / 2
        sat_in_view_flag = 0
        time_delta = timedelta(seconds=1)  # timedelta to check new azimuth, if we move to more granular seconds takes FOREVER to run but get more windows
        for sat in self._list_of_satellites:
            enter_events = []
            exit_events = []
            rhodesmill_earthsat = sat.to_rhodesmill()
            difference = rhodesmill_earthsat - coordinates
            for point in self._path:
                starting_interval = point.time
                ending_interval = point.time + timedelta(minutes=1)
                while starting_interval < ending_interval:
                    topocentric = difference.at(ts.from_datetime(point.time))
                    alt, az, distance = topocentric.altaz()
                    satellite_altitude = alt.degrees
                    satellite_azimuth = min(az.degrees, 360 - az.degrees)
                    if (point.altitude.degree - half_beamwidth) <= satellite_altitude <= (point.altitude.degree + half_beamwidth):
                            if (point.azimuth.degree - half_beamwidth) <= satellite_azimuth <= (point.azimuth.degree + half_beamwidth) and sat_in_view_flag == 0:
                                enter_events.append(convert_datetime_to_utc(point.time))
                            elif (satellite_azimuth > (point.azimuth.degree + half_beamwidth)) or (satellite_azimuth < (point.azimuth.degree - half_beamwidth)):
                                if sat_in_view_flag == 1:
                                    exit_events.append(convert_datetime_to_utc(point.time))
                    starting_interval+=time_delta
            if enter_events != exit_events:
                exit_events.append(self._reservation.time.end)
            enter_and_exit_pairs = zip(enter_events, exit_events)
            time_windows = [TimeWindow(begin=begin_event, end=exit_event) for begin_event, exit_event in enter_and_exit_pairs]
            overhead_windows = [OverheadWindow(satellite=sat, overhead_time=time_window) for
                                time_window in time_windows]
            for window in overhead_windows:
                azimuth_filtered_overhead_windows.append(window)
        return azimuth_filtered_overhead_windows
