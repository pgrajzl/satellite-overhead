from datetime import datetime, timezone
from typing import List

import pytz

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.satellite.international_designator import InternationalDesignator
from satellite_determination.custom_dataclasses.satellite.mean_motion import MeanMotion
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.satellite.tle_information import TleInformation
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder import EventFinder
from satellite_determination.main import Main, MainResults


class EventFinderForTestingMain(EventFinder):

    def get_overhead_windows(self) -> List[OverheadWindow]:
        pass

    def get_overhead_windows_slew(self) -> List[OverheadWindow]:
        pass


class TestMain:
    def test_arbitrary_inputs_match_expected_output(self):
        result = Main(reservation=self._arbitrary_reservation,
                      satellites=self._satellites).run()
        assert result == MainResults(
            satellites_above_horizon=[OverheadWindow(satellite=self._satellite_in_mainbeam,
                                                     overhead_time=TimeWindow(begin=datetime(2023, 3, 30, 14, 38, tzinfo=timezone.utc),
                                                     end=datetime(2023, 3, 30, 14, 40, tzinfo=timezone.utc))),
                                      OverheadWindow(
                                          satellite=self._satellite_inside_frequency_range_and_above_horizon_and_outside_mainbeam,
                                          overhead_time=TimeWindow(
                                              begin=datetime(2023, 3, 30, 14, 39, 34, 791130, tzinfo=timezone.utc),
                                              end=datetime(2023, 3, 30, 14, 38, 0, 0, tzinfo=timezone.utc))),

                                      ],
            interference_windows=[OverheadWindow(satellite=self._satellite_in_mainbeam,
                                                 overhead_time=TimeWindow(begin=datetime(2023, 3, 30, 14, 38, tzinfo=timezone.utc),
                                                                          end=datetime(2023, 3, 30, 14, 40, tzinfo=timezone.utc)))])

    @property
    def _arbitrary_reservation(self) -> Reservation:
        return Reservation(
            facility=Facility(
                right_ascension='4h42m',
                coordinates=Coordinates(latitude=40.8178049, longitude=-121.4695413),
                name='ARBITRARY_1',
                declination='-38d6m50.8s',
            ),
            time=self._arbitrary_search_window,
            frequency=FrequencyRange(
                frequency=135,
                bandwidth=10
            )
        )

    @property
    def _satellites(self):
        return [
            self._satellite_in_mainbeam,
            self._satellite_inside_frequency_range_and_above_horizon_and_outside_mainbeam,
            self._satellite_inside_frequency_range_and_below_horizon,
            self._satellite_outside_frequency_range
        ]
    
    @property
    def _satellite_in_mainbeam(self) -> Satellite:
        return Satellite(name='SAUDISAT 2',
                         tle_information=TleInformation(argument_of_perigee=2.6581678667138995,
                                                        drag_coefficient=8.4378e-05,
                                                        eccentricity=0.0025973,
                                                        epoch_days=26801.46955532,
                                                        inclination=1.7179345640550268,
                                                        international_designator=InternationalDesignator(year=4,
                                                                                                         launch_number=25,
                                                                                                         launch_piece='F'),
                                                        mean_anomaly=3.6295308619113436,
                                                        mean_motion=MeanMotion(first_derivative=9.605371056982682e-12,
                                                                               second_derivative=0.0,
                                                                               value=0.06348248105551128),
                                                        revolution_number=200,
                                                        right_ascension_of_ascending_node=1.7778098293739442,
                                                        satellite_number=28371,
                                                        classification='U'),
                         frequency=[FrequencyRange(frequency=137.513, bandwidth=None, status='active')])

    @property
    def _satellite_inside_frequency_range_and_above_horizon_and_outside_mainbeam(self) -> Satellite:
        return Satellite(name='NOAA 15',
                         tle_information=TleInformation(argument_of_perigee=0.8036979406046088,
                                                        drag_coefficient=0.00010892000000000001,
                                                        eccentricity=0.0011139, epoch_days=26801.4833696,
                                                        inclination=1.7210307781480645,
                                                        international_designator=InternationalDesignator(
                                                            year=98, launch_number=30, launch_piece='A'),
                                                        mean_anomaly=5.4831490673456615,
                                                        mean_motion=MeanMotion(
                                                            first_derivative=6.6055864051174274e-12,
                                                            second_derivative=0.0,
                                                            value=0.06223475712876591),
                                                        revolution_number=30102,
                                                        right_ascension_of_ascending_node=2.932945522830879,
                                                        satellite_number=25338, classification='U'),
                         frequency=[FrequencyRange(frequency=137.62, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=137.5, bandwidth=None, status='inactive'),
                                    FrequencyRange(frequency=137.77, bandwidth=None, status='inactive'),
                                    FrequencyRange(frequency=1544.5, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=1702.5, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=465.9875, bandwidth=None, status='invalid'),
                                    FrequencyRange(frequency=137.35, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=2247.5, bandwidth=None, status='active')])

    @property
    def _satellite_inside_frequency_range_and_below_horizon(self) -> Satellite:
        return Satellite(name='ISS (ZARYA)', 
                         tle_information=TleInformation(argument_of_perigee=6.2680236319675116, 
                                                        drag_coefficient=0.00018991,
                                                        eccentricity=0.0006492, 
                                                        epoch_days=26801.40295236, 
                                                        inclination=0.9012601004618398,
                                                        international_designator=InternationalDesignator(year=98, 
                                                                                                         launch_number=67, 
                                                                                                         launch_piece='A'), 
                                                        mean_anomaly=0.0168668618912732, 
                                                        mean_motion=MeanMotion(first_derivative=3.185528893440345e-10, 
                                                                               second_derivative=0.0, 
                                                                               value=0.06764422624907401), 
                                                        revolution_number=39717, 
                                                        right_ascension_of_ascending_node=2.027426818994173, 
                                                        satellite_number=25544, 
                                                        classification='U'), 
                         frequency=[FrequencyRange(frequency=437.525, bandwidth=None, status='inactive'),
                                    FrequencyRange(frequency=468.1, bandwidth=None, status='invalid'), 
                                    FrequencyRange(frequency=145.8, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=130.167, bandwidth=None, status='active'), 
                                    FrequencyRange(frequency=437.8, bandwidth=None, status='active'), 
                                    FrequencyRange(frequency=2213.5, bandwidth=None, status='active'), 
                                    FrequencyRange(frequency=437.8, bandwidth=None, status='active'), 
                                    FrequencyRange(frequency=400.575, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=2216.0, bandwidth=None, status='active'), 
                                    FrequencyRange(frequency=637.5, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=2265.0, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=137.6257, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=143.625, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=145.825, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=632.0, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=437.023, bandwidth=None, status='inactive'),
                                    FrequencyRange(frequency=400.5, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=630.128, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=145.8, bandwidth=None, status='invalid'),
                                    FrequencyRange(frequency=435.4, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=145.8, bandwidth=None, status='inactive'),
                                    FrequencyRange(frequency=437.05, bandwidth=None, status='inactive'),
                                    FrequencyRange(frequency=121.1, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=2205.5, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=145.48, bandwidth=None, status='inactive'),
                                    FrequencyRange(frequency=145.825, bandwidth=None, status='inactive'),
                                    FrequencyRange(frequency=121.75, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=468.1, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=2425.0, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=145.8, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=2375.0, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=417.1, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=414.2, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=437.55, bandwidth=None, status='inactive'),
                                    FrequencyRange(frequency=437.8, bandwidth=None, status='invalid'),
                                    FrequencyRange(frequency=145.8, bandwidth=None, status='inactive'),
                                    FrequencyRange(frequency=121.275, bandwidth=None, status='active')])

    @property
    def _satellite_outside_frequency_range(self) -> Satellite:
        return Satellite(name='EYESAT A (AO-27)',
                         tle_information=TleInformation(argument_of_perigee=2.6114942718570675, drag_coefficient=6.5858e-05,
                                                        eccentricity=0.0009025, epoch_days=26801.12744469,
                                                        inclination=1.7251410285365112,
                                                        international_designator=InternationalDesignator(year=93,
                                                                                                         launch_number=61,
                                                                                                         launch_piece='C'),
                                                        mean_anomaly=3.674670312355673,
                                                        mean_motion=MeanMotion(first_derivative=3.787606883668251e-12,
                                                                               second_derivative=0.0,
                                                                               value=0.06240853642079434),
                                                        revolution_number=54626,
                                                        right_ascension_of_ascending_node=3.150839407966859,
                                                        satellite_number=22825, classification='U'),
                         frequency=[FrequencyRange(frequency=436.795, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=436.795, bandwidth=None, status='active'),
                                    FrequencyRange(frequency=2218.0, bandwidth=None, status='active')])
