import pytz
import datetime
import os
from pathlib import Path
from datetime import datetime
import filecmp

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesMill
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.custom_dataclasses.frequency_range import FrequencyRange
from tests.utilities import get_script_directory


class TestWindowListFinder:

    def test_get_window_list(self):
        tle_file = Path(get_script_directory(__file__), 'test_tle_data', 'arbitrary_TLE.txt')
        frequency_file = Path(get_script_directory(__file__), 'fake_ISS_frequency_file_multiple.csv')
        list_of_satellites = Satellite.from_tle_file(tlefilepath=tle_file, frequencyfilepath=frequency_file) #load satellites from arbitrary TLE file
        reservation = Reservation(facility=Facility(elevation=0, point_coordinates=Coordinates(latitude=40.8178049, longitude=-121.4695413), name='name', azimuth=30),
                                  time=TimeWindow(begin=datetime(year=2023, month=2, day=22, hour=1, tzinfo=pytz.utc), end=datetime(year=2023, month=2, day=22, hour=2, tzinfo=pytz.utc)),
                                  frequency=FrequencyRange(
                                      frequency=None,
                                      bandwidth=None
                                  )
                                  )
        overhead_windows = EventFinderRhodesMill(list_of_satellites=list_of_satellites, reservation=reservation).get_overhead_windows()
        print(len(overhead_windows))
        with open ("satellite_overhead_test", "w") as outfile:
            outfile.writelines(str(overhead_windows))
            outfile.close()

        assert filecmp.cmp('./tests/event_finder/test_reference_files/overhead_window_reference.txt', 'satellite_overhead_test') == 1
        os.remove("satellite_overhead_test")

TestWindowListFinder().test_get_window_list()

