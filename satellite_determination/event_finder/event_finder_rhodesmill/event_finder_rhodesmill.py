from datetime import timedelta
from typing import List

import pytz
from skyfield.api import load, wgs84, Time
from satellite_determination.azimuth_filter.azimuth_filtering import AzimuthFilter
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder_rhodesmill.support.overhead_window_from_events import \
    EventRhodesmill, EventTypesRhodesmill, OverheadWindowFromEvents
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.observation_path import ObservationPath

class EventFinderRhodesMill:

    def __init__(self, list_of_satellites: List[Satellite], reservation: Reservation, azimuth_altitude_path: List[ObservationPath]):
        self._list_of_satellites = list_of_satellites
        self._reservation = reservation
        self._path = azimuth_altitude_path

    def get_overhead_windows(self):
        ts = load.timescale() #provides time objects with the data tables they need to translate between different time scales: the schedule of UTC leap seconds, and the value of ∆T over time.
        overhead_windows = []
        t0 = ts.from_datetime(self._reservation.time.begin.replace(tzinfo=pytz.UTC))  # changes the reservation datetime to Skyfield Time object
        t1 = ts.from_datetime(self._reservation.time.end.replace(tzinfo=pytz.UTC))
        coordinates = wgs84.latlon(self._reservation.facility.point_coordinates.latitude, self._reservation.facility.point_coordinates.longitude)
        for sat in self._list_of_satellites:
            rhodesmill_earthsat = sat.to_rhodesmill() #convert from custom satellite class to Rhodesmill EarthSatellite
            t, events = rhodesmill_earthsat.find_events(coordinates, t0, t1, altitude_degrees=self._reservation.facility.altitude)
            if events.size == 0:
                continue
            else:
                rhodesmill_event_list = []
                for ti, event in zip(t, events):
                    if event == 0:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.ENTERS, satellite=sat, timestamp=ti.utc_datetime())
                    elif event == 1:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.CULMINATES, satellite=sat, timestamp=ti.utc_datetime())
                    elif event == 2:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.EXITS, satellite=sat, timestamp=ti.utc_datetime())
                    rhodesmill_event_list.append(translated_event)
                sat_windows = OverheadWindowFromEvents(events=rhodesmill_event_list, reservation=self._reservation).get() #passes as custom dataclass Satellite
                for window in sat_windows:
                    overhead_windows.append(window)
        azimuth_filtered_windows = AzimuthFilter(overhead_windows=overhead_windows, reservation=self._reservation).filter_azimuth()
        return azimuth_filtered_windows

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
                                enter_events.append(point.time)
                            elif (satellite_azimuth > (point.azimuth.degree + half_beamwidth)) or (satellite_azimuth < (point.azimuth.degree - half_beamwidth)):
                                if sat_in_view_flag == 1:
                                    exit_events.append(point.time)
                    point.time+=time_delta
            if enter_events != exit_events:
                exit_events.append(self._reservation.time.end)
            enter_and_exit_pairs = zip(enter_events, exit_events)
            time_windows = [TimeWindow(begin=begin_event, end=exit_event) for begin_event, exit_event in enter_and_exit_pairs]
            overhead_windows = [OverheadWindow(satellite=sat, overhead_time=time_window) for
                                time_window in time_windows]
            azimuth_filtered_overhead_windows.append(overhead_windows)
        return azimuth_filtered_overhead_windows

