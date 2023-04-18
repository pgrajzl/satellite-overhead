from datetime import datetime
from pathlib import Path
from typing import List

import pytz
from skyfield.api import EarthSatellite, Time

from satellite_determination.azimuth_filter.azimuth_filtering import AzimuthFilter
from satellite_determination.custom_dataclasses.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.satellite.international_designator import InternationalDesignator
from satellite_determination.custom_dataclasses.satellite.mean_motion import MeanMotion
from satellite_determination.custom_dataclasses.satellite.tle_information import TleInformation
from tests.utilities import get_script_directory
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.time_window import TimeWindow


class TestAzimuthFilter:
    def test_single_sat(self):
        windows = AzimuthFilter(overhead_windows=[self._arbitrary_overhead_window], reservation=self._arbitrary_reservation).filter_azimuth()
        assert windows == self._expected_windows


    @property
    def _arbitrary_reservation(self) -> Reservation:
        return Reservation(facility=Facility(elevation=0,
                                             point_coordinates=Coordinates(latitude=40.8178049, longitude=-121.4695413),
                                             azimuth=30,
                                             name='name'),
                           time=TimeWindow(begin=datetime(year=2023, month=2, day=1, hour=1),
                                           end=datetime(year=2023, month=2, day=1, hour=6)),
                           frequency=FrequencyRange(
                               frequency=None,
                               bandwidth=None
                           )
                           )
    @property
    def _arbitrary_overhead_window(self) -> OverheadWindow:
        return OverheadWindow(satellite=self._arbitrary_satellite[0], overhead_time=TimeWindow(begin=self._arbitrary_date, end=self._arbitrary_date_two))

    @property
    def _arbitrary_satellite(self) -> EarthSatellite:
        tle_file = Path(get_script_directory(__file__), 'test_tle_data', 'single_TLE.txt')
        frequency_file = Path(get_script_directory(__file__), 'fake_ISS_frequency_file_multiple.csv')
        arbitrary_satellite = Satellite.from_tle_file(tlefilepath=tle_file, frequencyfilepath=frequency_file)
        return arbitrary_satellite

    @property
    def _arbitrary_date(self) -> Time:
        return datetime(year=2023, month=1, day=1, hour=1, tzinfo=pytz.utc)

    @property
    def _arbitrary_date_two(self) -> datetime:
        return datetime(year=2023, month=1, day=1, hour=3, tzinfo=pytz.utc)

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
                frequency=[FrequencyRange(frequency=None, bandwidth=None, status=None)]
            )

    @property
    def _expected_windows(self) -> List[OverheadWindow]:
        return [OverheadWindow(
            satellite=self._COSMOS_DEB,
            overhead_time=TimeWindow(
                begin=datetime(2023, 1, 1, 2, 16, 58, tzinfo=pytz.utc),
                end=datetime(2023, 1, 1, 2, 17, 49, tzinfo=pytz.utc)
            )
        ),

        OverheadWindow(
                satellite=self._COSMOS_DEB,
                overhead_time=TimeWindow(
                    begin=datetime(2023, 1, 1, 2, 35, 20, tzinfo=pytz.utc),
                    end=datetime(2023, 1, 1, 2, 36, 21, tzinfo=pytz.utc)
                )
            )
        ]
