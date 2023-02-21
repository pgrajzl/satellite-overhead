from datetime import datetime, timedelta
from typing import List

import pytz
from skyfield.api import wgs84
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.time_window import TimeWindow

class TestAzimuthFiltering:

    def __init__(self, overhead_windows: List[OverheadWindow], reservation: Reservation):
        self._overhead_windows = overhead_windows
        self._reservation = reservation

    def filter_azimuth(self) -> List[OverheadWindow]:
        overhead_windows = []
        enter_events = []
        exit_events = []
        sat_in_view_flag = 0
        coordinates = wgs84.latlon(self._reservation.facility.point_coordinates.latitude,
                                   self._reservation.facility.point_coordinates.longitude)
        time_delta = timedelta(minutes=1)
        for window in self._overhead_windows:
            difference = window.satellite - coordinates  # get vector sat relative to telescope location
            while window.overhead_time.begin.astimezone(pytz.utc) < window.overhead_time.end.astimezone(pytz.utc):  # timestamp for events needs to be changed since when the sat enters cone is not necessarily event timestamp
                topocentric = difference.at(window.overhead_time.begin)
                alt, az, distance = topocentric.altaz()
                if (az.degrees < (self._reservation.facility.azimuth + 1.5)) and (az.degrees > (self._reservation.facility.azimuth - 1.5)):
                    if sat_in_view_flag == 0:
                        enter_events.append(window.overhead_time.begin)
                        sat_in_view_flag = 1
                elif (az.degrees < (self._reservation.facility.azimuth + 1.5)) or (az.degrees > (self._reservation.facility.azimuth - 1.5)) and (sat_in_view_flag == 1):
                        exit_events.append(window.overhead_time.begin)
                        sat_in_view_flag = 0
                window.overhead_time.begin += time_delta
            if enter_events != exit_events:
                exit_events.append(self._reservation.time.end)
            enter_and_exit_pairs = zip(enter_events, exit_events)
            time_windows = [TimeWindow(begin=begin_event, end=exit_event) for begin_event, exit_event in enter_and_exit_pairs]
            overhead_windows_sat = [OverheadWindow(satellite=window.satellite, overhead_time=time_window) for time_window in time_windows]
            for new_window in overhead_windows_sat:
                print(new_window.satellite)
                print(new_window.overhead_time.begin.astimezone(pytz.utc))
                print(new_window.overhead_time.end.astimezone(pytz.utc))
                overhead_windows.append(new_window)
        return overhead_windows
