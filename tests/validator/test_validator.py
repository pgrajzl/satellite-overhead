from skyfield.api import load, wgs84
import datetime
import os
from pathlib import Path
from datetime import datetime
import json
import filecmp

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.retrievers.satellite_retriever.skyfield_satellite_retriever import SkyfieldSatelliteList
from satellite_determination.validator.validator import Validator
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.utilities import convert_dt_to_utc
from tests.utilities import get_script_directory
from tests.validator.test_overhead_from_events import EventRhodesmill


class TestValidatorRhodesMill(Validator):

    def overhead_list(self, list_of_satellites: SkyfieldSatelliteList, reservation: Reservation):
        ts = load.timescale()
        overhead_windows = []
        t0 = ts.utc(convert_dt_to_utc(reservation.time.begin))
        t1 = ts.utc(convert_dt_to_utc(reservation.time.end))
        coordinates = wgs84.latlon(reservation.facility.point_coordinates.latitude, reservation.facility.point_coordinates.longitude)
        for sat in list_of_satellites.satellites:
            t, events = sat.find_events(coordinates, t0, t1, altitude_degrees=reservation.facility.angle_of_visibility_cone)
            rhodesmill_event_list = []
            if events.size == 0:
                continue
            else:
                #skeleton
                for ti, event in zip(t, events):
                    translated_event = EventRhodesmill
                    translated_event.event_type = event
                    translated_event.satellite = sat
                    translated_event.timestamp = ti
                    rhodesmill_event_list.append(translated_event)
                overhead_windows.append().get(events=rhodesmill_event_list, reservation=Reservation)
        return overhead_windows

    def test_can_get_overhead_list(self):
        tle_file = Path(get_script_directory(__file__), 'TLEdata', 'test.txt')
        list_of_satellites = SkyfieldSatelliteList.load_tle(str(tle_file))
        reservation = self._arbitrary_reservation
        interferers = self.overhead_list(list_of_satellites, reservation)
        dict = {
            "satellite_name": []
        }
        for interferer in interferers:
                print(interferer.satellite.name)
                dict["satellite_name"].append(interferer.satellite.name)
        with open ("satellite_overhead_test", "a") as outfile:
            json.dump(dict, outfile)
            outfile.close()
        assert filecmp.cmp('./tests/validator/satellite_reference_file', 'satellite_overhead_test') == 1
        os.remove("satellite_overhead_test")

    @property
    def _arbitrary_reservation(self) -> Reservation:
        return Reservation(facility=Facility(angle_of_visibility_cone=20.1,
                                             point_coordinates=Coordinates(latitude=4., longitude=5.),
                                             name='ArbitraryFacilityName2'),
                           time=TimeWindow(begin=datetime(year=2022, month=12, day=1, hour=16, minute=0), end=datetime(year=2022, month=12, day=2, hour=16, minute=0)))

    @property
    def _arbitrary_sat_list(self) -> :




'''
                for ti, event in zip(t, events):
                    if event == 0:
                        begin = ti
                    elif event == 2:
                        end = ti
                time_window = TimeWindow(begin, end)
                overhead = OverheadWindow(sat, time_window)
                interferers.append(overhead)
'''
