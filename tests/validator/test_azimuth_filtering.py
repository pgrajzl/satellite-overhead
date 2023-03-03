from datetime import datetime, timedelta
from typing import List

import pytz
from skyfield.api import wgs84
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from tests.validator.test_overhead_window_from_azimuth import OverheadWindowFromAzimuth

class TestAzimuthFiltering:

    def __init__(self, overhead_windows: List[OverheadWindow], reservation: Reservation):
        self._overhead_windows = overhead_windows
        self._reservation = reservation

    def filter_azimuth(self) -> List[OverheadWindow]:
        azimuth_filtered_overhead_windows = []
        coordinates = wgs84.latlon(self._reservation.facility.point_coordinates.latitude,
                                   self._reservation.facility.point_coordinates.longitude)
        time_delta = timedelta(minutes=1) #timedelta to check new azimuth
        for window in self._overhead_windows:
            difference = window.satellite - coordinates  # get vector sat relative to telescope location
            while window.overhead_time.begin.astimezone(pytz.utc) < window.overhead_time.end.astimezone(pytz.utc):  # timestamp for events needs to be changed since when the sat enters cone is not necessarily event timestamp
                topocentric = difference.at(window.overhead_time.begin)
                alt, az, distance = topocentric.altaz()
                satellite_azimuth = min(az.degrees, 360 - az.degrees)
                satellite_azimuth_values.append(satellite_azimuth)
                satellite_time_values.append(window.overhead_time.begin)
                window.overhead_time.begin += time_delta
            azimuth_time_pairs = zip(satellite_azimuth_values, satellite_time_values)
            windows = OverheadWindowFromAzimuth(azimuth_time_pairs, self._reservation, window).get_window_from_azimuth()
            for new_window in windows:
                azimuth_filtered_overhead_windows.append(new_window)
        for new_window in azimuth_filtered_overhead_windows:
            print(new_window.satellite)
            print(new_window.overhead_time.begin.astimezone(pytz.utc))
            print(new_window.overhead_time.end.astimezone(pytz.utc))
        return azimuth_filtered_overhead_windows
