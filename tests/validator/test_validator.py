from skyfield.api import load, wgs84
import datetime
import sys
import numpy as nps
from datetime import datetime
from satellite_determination.dataclasses.coordinates import Coordinates
from satellite_determination.dataclasses.facility import Facility
from satellite_determination.dataclasses.time_window import TimeWindow
from satellite_determination.dataclasses.reservation import Reservation
from satellite_determination.dataclasses.overhead_window import OverheadWindow
from satellite_determination.dataclasses.skyfield_satellite import SkyfieldSatelliteList
from satellite_determination.validator.validator import Validator
from satellite_determination.dataclasses.time_window import TimeWindow

from skyfield.timelib import Timescale
from skyfield.api import utc

class ValidatorRhodesMill(Validator):

    def overhead_list(self, list_of_satellites: SkyfieldSatelliteList, reservation: Reservation):
        ts = load.timescale()
        interferers = []
        #t0 = ts.utc(ts.from_datetime(reservation.time.begin)) #ts.utc(reservation.time.begin)
        #t1 = ts.utc(ts.from_datetime(reservation.time.end)) #ts.utc(reservation.time.end)
        t0 = ts.utc(reservation.time.begin.replace(tzinfo=utc))
        t1 = ts.utc(reservation.time.end.replace(tzinfo=utc))
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

    def test_can_get_overhead_list(self):
        list_of_satellites = SkyfieldSatelliteList.load_tle('TLEdata/test.txt')
        reservation = Reservation(
                facility=Facility(
                    angle_of_visibility_cone=20.1,
                    point_coordinates=Coordinates(latitude=4., longitude=5.),
                    name='ArbitraryFacilityName2'
                ),
                time=TimeWindow(
                    begin=datetime(year=2022, month=12, day=30, hour=16),
                    end=datetime(year=2022, month=12, day=30, hour=17)
                )
        )
        interferers = self.overhead_list(list_of_satellites, reservation)
        for interferer in interferers:
            print(interferer)


validator = ValidatorRhodesMill()
validator.test_can_get_overhead_list()