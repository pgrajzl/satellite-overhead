from skyfield.api import load, wgs84
import datetime
import sys
import numpy as nps
from satellite_determination.dataclasses.reservation import Reservation
from satellite_determination.dataclasses.overhead_window import OverheadWindow
from satellite_determination.retrievers.satellite_retriever.skyfield_satellite_retriever import SkyfieldSatelliteList
from satellite_determination.validator.validator import Validator
from satellite_determination.dataclasses.time_window import TimeWindow
from satellite_determination.utilities import convert_tz_to_utc
from skyfield.timelib import Timescale
from skyfield.api import utc

class ValidatorRhodesMill(Validator):

    def overhead_list(self, list_of_satellites: SkyfieldSatelliteList, reservation: Reservation):
        ts = load.timescale()
        interferers = []
        t0 = ts.utc(convert_tz_to_utc(reservation.time.begin))
        t1 = ts.utc(convert_tz_to_utc(reservation.time.end))
        coordinates = wgs84.latlon(reservation.facility.point_coordinates.latitude, reservation.facility.point_coordinates.longitude)
        for sat in list_of_satellites.satellites:
            t, events = sat.find_events(coordinates, t0, t1, altitude_degrees=reservation.facility.angle_of_visibility_cone)
            if events.size == 0:
                continue
            else:
                for ti, event in zip(t, events):
                    if event == 0:
                        begin = ti
                    elif event == 2:
                        end = ti
                time_window = TimeWindow(begin, end)
                overhead = OverheadWindow(sat, time_window)
                interferers.append(overhead)
        return interferers

