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
#from satellite_determination.validator.validator import Validator
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.utilities import convert_dt_to_utc
from tests.utilities import get_script_directory
from tests.validator.test_overhead_from_events import EventRhodesmill, OverheadWindowFromEvents, EventTypesRhodesmill


class ValidatorRhodesMill:

    def __init__(self, list_of_satellites: SkyfieldSatelliteList, reservation: Reservation):
        self._list_of_satellites = list_of_satellites
        self._reservation = reservation

    def get_overhead_windows(self):
        ts = load.timescale()
        overhead_windows = []
        t0 = ts.utc(convert_dt_to_utc(self._reservation.time.begin))
        t1 = ts.utc(convert_dt_to_utc(self._reservation.time.end))
        coordinates = wgs84.latlon(self._reservation.facility.point_coordinates.latitude, self._reservation.facility.point_coordinates.longitude)
        for sat in self._list_of_satellites.satellites:
            print(sat.name)
            t, events = sat.find_events(coordinates, t0, t1, altitude_degrees=self._reservation.facility.angle_of_visibility_cone)
            if events.size == 0:
                print("no events")
                continue
            else:
                #skeleton
                rhodesmill_event_list = []
                for ti, event in zip(t, events):
                    #print(event)
                    if event == 0:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.ENTERS, satellite=sat, timestamp=ti)
                    elif event == 1:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.CULMINATES, satellite=sat, timestamp=ti)
                    elif event == 2:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.EXITS, satellite=sat, timestamp=ti)
                    rhodesmill_event_list.append(translated_event)
                for event in rhodesmill_event_list:
                    print(event.event_type)
                sat_windows = OverheadWindowFromEvents(events=rhodesmill_event_list, reservation=self._reservation).get()
                for window in sat_windows:
                    overhead_windows.append(window)
                if len(sat_windows) != 0:
                    print(sat_windows)
                else:
                    print("none")
        #print(overhead_windows[0].overhead_time)
        return overhead_windows


class TestWindowListFinder:

    def test_get_window_list(self):
        tle_file = Path(get_script_directory(__file__), 'TLEdata', 'arbitrary_TLE.txt')
        list_of_satellites = SkyfieldSatelliteList.load_tle(str(tle_file))
        reservation = Reservation(facility=Facility(angle_of_visibility_cone=0, point_coordinates=Coordinates(latitude=0, longitude=0),name='name'),
                                  time=TimeWindow(begin=datetime(year=2023, month=2, day=14, hour=1), end=datetime(year=2023, month=2, day=14, hour=6)))
        overhead_windows = ValidatorRhodesMill(list_of_satellites=list_of_satellites, reservation=reservation).get_overhead_windows()

        for window in overhead_windows:
            print("test")
            print(window)
            #dict["satellite"].append(window.satellite)
            #dict["overhead_time"].append(window.overhead_time)
        #with open ("satellite_overhead_test", "a") as outfile:
            #json.dump(dict, outfile)
            #outfile.close()
        #assert filecmp.cmp('./tests/validator/satellite_reference_file', 'satellite_overhead_test') == 1
        #os.remove("satellite_overhead_test")

    #@property
    #def _arbitrary_reservation(self) -> Reservation:
        #return Reservation(facility=Facility(angle_of_visibility_cone=0,
                                            #point_coordinates=Coordinates(latitude=0, longitude=0),
                                            # name='name'),
                           #time=TimeWindow(begin=datetime(year=2001, month=2, day=1, hour=1), end=datetime(year=2001, month=2, day=1, hour=6)))

TestWindowListFinder.test_get_window_list(TestWindowListFinder)



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
