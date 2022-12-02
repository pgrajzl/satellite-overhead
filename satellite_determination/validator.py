from skyfield.api import load, wgs84
import datetime
import sys
import numpy as nps
from satellite_determination.dataclasses.reservation import Reservation
from satellite_determination.dataclasses.overhead_window import OverheadWindow
from satellite_determination.dataclasses.satellite import Satellite
from satellite_determination.validator.validator import Validator
from satellite_determination.dataclasses.time_window import TimeWindow


class ValidatorRhodesMill(Validator):

    def overhead_list(self, list_of_satellites, reservation):
        ts = load.timescale()
        interferers = []
        t0 = ts.utc(reservation.time_start)
        t1 = ts.utc(reservation.time_end)
        satellites = load.tle_file("./TLEData/")
        coordinates = wgs84.latlon(reservation.point_coordinates.latitude, reservation.point_coordinates.longitude)
        for sat in satellites:
            t, events = sat.find_events(coordinates, t0, t1, altitude_degrees=reservation.Facility.angle_of_visibility_cone)
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

