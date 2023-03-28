import pytz
import datetime
import os
from pathlib import Path
from datetime import datetime
import filecmp
from typing import List

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesMill
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.satellite.tle_information import TleInformation
from satellite_determination.custom_dataclasses.satellite.mean_motion import MeanMotion
from satellite_determination.custom_dataclasses.satellite.international_designator import InternationalDesignator
from tests.utilities import get_script_directory


class TestWindowListFinder:

    def test_get_window_list(self):
        tle_file = Path(get_script_directory(__file__), 'TestTLEdata', 'arbitrary_TLE.txt')
        list_of_satellites = Satellite.from_tle_file(tle_file) #load satellites from arbitrary TLE file
        reservation = Reservation(facility=Facility(elevation=0, point_coordinates=Coordinates(latitude=40.8178049, longitude=-121.4695413),name='name', azimuth=30),
                                  time=TimeWindow(begin=datetime(year=2023, month=2, day=22, hour=1, tzinfo=pytz.utc), end=datetime(year=2023, month=2, day=22, hour=2, tzinfo=pytz.utc)))
        overhead_windows = EventFinderRhodesMill(list_of_satellites=list_of_satellites, reservation=reservation).get_overhead_windows()
        assert overhead_windows == self._expected_windows

    @property
    def _COSMOS_DEB(self) -> Satellite:
        return Satellite(
                name='0 COSMOS 1932 DEB',
                tle_information=TleInformation(
                    argument_of_perigee=5.153187590939126,
                    drag_coefficient=0.00015211,
                    eccentricity=0.0057116,
                    epoch_days=26633.28893622,
                    inclination=1.1352005427406557,
                    international_designator=InternationalDesignator(
                        year=88,
                        launch_number=19,
                        launch_piece='F'
                    ),
                    mean_anomaly=4.188343400497881,
                    mean_motion=MeanMotion(
                        first_derivative=2.363466695408988e-12,
                        second_derivative=0.0,
                        value=0.060298700041442894
                    ),
                    revolution_number=95238,
                    right_ascension_of_ascending_node=2.907844197528697,
                    satellite_number=28275,
                    classification='U'
                ),
                frequency=None
            )

    @property
    def _ROCSAT(self) -> Satellite:
        return Satellite(
                name='0 ROCSAT 2',
                tle_information=TleInformation(
                    argument_of_perigee=0.04651476989490087,
                    drag_coefficient=-1.9462e-05,
                    eccentricity=0.0002373,
                    epoch_days=26633.80795892,
                    inclination=1.7218807534937857,
                    international_designator=InternationalDesignator(
                        year=4,
                        launch_number=18,
                        launch_piece='A'
                    ),
                    mean_anomaly=2.985923246945915,
                    mean_motion=MeanMotion(
                        first_derivative=-2.12105985485422e-12,
                        second_derivative=0.0,
                        value=0.06111631248860934
                    ),
                    revolution_number=94766,
                    right_ascension_of_ascending_node=5.859763194658006,
                    satellite_number=28254,
                    classification='U'
                ),
                frequency=None
            )

    @property
    def _expected_windows(self) -> List[OverheadWindow]:
        return [OverheadWindow(
            satellite=self._COSMOS_DEB,
            overhead_time=TimeWindow(
                begin=datetime(2023, 2, 22, 1, 20, 47, 182648, tzinfo=pytz.utc),
                end=datetime(2023, 2, 22, 1, 21, 19, 182648, tzinfo=pytz.utc)
            )
        ),

        OverheadWindow(
                satellite=self._COSMOS_DEB,
                overhead_time=TimeWindow(
                    begin=datetime(2023, 2, 22, 1, 28, 55, 182648, tzinfo=pytz.utc),
                    end=datetime(2023, 2, 22, 1, 29, 19, 182648, tzinfo=pytz.utc)
                )
            ),

        OverheadWindow(
                satellite=self._ROCSAT,
                overhead_time=TimeWindow(
                    begin=datetime(2023, 2, 22, 1, 49, 24, 954282, tzinfo=pytz.utc),
                    end=datetime(2023, 2, 22, 1, 50, 4, 954282, tzinfo=pytz.utc)
                )
            )
        ]

