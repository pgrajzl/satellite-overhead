from dataclasses import replace
from typing import List
import pytz
from pathlib import Path
from datetime import datetime, timedelta

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.frequency_range.support.get_frequency_data_from_csv import \
    GetFrequencyDataFromCsv
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.satellite.international_designator import InternationalDesignator
from satellite_determination.custom_dataclasses.satellite.mean_motion import MeanMotion
from satellite_determination.custom_dataclasses.satellite.tle_information import TleInformation
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesMill
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellite_position_with_respect_to_facility_retriever.satellite_position_with_respect_to_facility_retriever import \
    SatellitePositionWithRespectToFacilityRetriever
from satellite_determination.utilities import get_script_directory
from tests.definitions import SMALL_EPSILON

ARBITRARY_SATELLITE_ALTITUDE = 0
ARBITRARY_SATELLITE_AZIMUTH = 0

class SatellitePositionWithRespectToFacilityRetrieverStub(SatellitePositionWithRespectToFacilityRetriever):
    def run(self) -> PositionTime:
        return PositionTime(
            altitude=ARBITRARY_SATELLITE_ALTITUDE,
            azimuth=ARBITRARY_SATELLITE_AZIMUTH,
            time=self._timestamp
        )


class TestWindowListFinder:
    def test_single_satellite(self):
        arbitrary_satellite = Satellite(name='arbitrary')
        arbitrary_datetime = datetime.now(tz=pytz.utc)
        arbitrary_time_window = TimeWindow(begin=arbitrary_datetime,
                                           end=arbitrary_datetime + timedelta(seconds=2))
        arbitrary_reservation = Reservation(facility=Facility(coordinates=Coordinates(latitude=0, longitude=0)),
                                            time=arbitrary_time_window)
        event_finder = EventFinderRhodesMill(list_of_satellites=[arbitrary_satellite],
                                             reservation=arbitrary_reservation,
                                             antenna_direction_path=[PositionTime(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                                                                                  azimuth=ARBITRARY_SATELLITE_AZIMUTH,
                                                                                  time=arbitrary_datetime)],
                                             satellite_position_with_respect_to_facility_retriever_class=SatellitePositionWithRespectToFacilityRetrieverStub)
        windows = event_finder.get_overhead_windows_slew()
        assert windows == [OverheadWindow(satellite=arbitrary_satellite, overhead_time=arbitrary_time_window)]

    def test_multiple_satellites(self):
        arbitrary_satellites = [Satellite(name='arbitrary'), Satellite(name='arbitrary2')]
        arbitrary_datetime = datetime.now(tz=pytz.utc)
        arbitrary_time_window = TimeWindow(begin=arbitrary_datetime,
                                           end=arbitrary_datetime + timedelta(seconds=2))
        arbitrary_reservation = Reservation(facility=Facility(coordinates=Coordinates(latitude=0, longitude=0)),
                                            time=arbitrary_time_window)
        event_finder = EventFinderRhodesMill(list_of_satellites=arbitrary_satellites,
                                             reservation=arbitrary_reservation,
                                             antenna_direction_path=[PositionTime(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                                                                                  azimuth=ARBITRARY_SATELLITE_AZIMUTH,
                                                                                  time=arbitrary_datetime)],
                                             satellite_position_with_respect_to_facility_retriever_class=SatellitePositionWithRespectToFacilityRetrieverStub)
        windows = event_finder.get_overhead_windows_slew()
        assert windows == [OverheadWindow(satellite=satellite, overhead_time=arbitrary_time_window)
                           for satellite in arbitrary_satellites]

    def test_multiple_antenna_positions_with_azimuth_filtering(self):
        arbitrary_satellite = Satellite(name='arbitrary')
        arbitrary_datetime = datetime.now(tz=pytz.utc)
        arbitrary_time_window = TimeWindow(begin=arbitrary_datetime,
                                           end=arbitrary_datetime + timedelta(seconds=3))
        arbitrary_reservation = Reservation(facility=Facility(coordinates=Coordinates(latitude=0, longitude=0)),
                                            time=arbitrary_time_window)
        altitude_outside_beamwidth = ARBITRARY_SATELLITE_ALTITUDE + arbitrary_reservation.facility.half_beamwidth + SMALL_EPSILON
        event_finder = EventFinderRhodesMill(list_of_satellites=[arbitrary_satellite],
                                             reservation=arbitrary_reservation,
                                             antenna_direction_path=[
                                                 PositionTime(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                                                              azimuth=ARBITRARY_SATELLITE_AZIMUTH,
                                                              time=arbitrary_datetime),
                                                 PositionTime(altitude=altitude_outside_beamwidth,
                                                              azimuth=ARBITRARY_SATELLITE_AZIMUTH,
                                                              time=arbitrary_datetime + timedelta(seconds=1)),
                                                 PositionTime(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                                                              azimuth=ARBITRARY_SATELLITE_AZIMUTH,
                                                              time=arbitrary_datetime + timedelta(seconds=2))
                                             ],
                                             satellite_position_with_respect_to_facility_retriever_class=SatellitePositionWithRespectToFacilityRetrieverStub)
        windows = event_finder.get_overhead_windows_slew()
        assert windows == [
            OverheadWindow(satellite=arbitrary_satellite, overhead_time=TimeWindow(begin=arbitrary_datetime,
                                                                                   end=arbitrary_datetime + timedelta(seconds=1))),
            OverheadWindow(satellite=arbitrary_satellite, overhead_time=TimeWindow(begin=arbitrary_datetime + timedelta(seconds=2),
                                                                                   end=arbitrary_datetime + timedelta(seconds=3)))
        ]

    def test_get_window_list(self):
        tle_file = Path(get_script_directory(__file__), '../test_tle_data', 'arbitrary_TLE.txt')
        frequency_file = Path(get_script_directory(__file__), '../fake_ISS_frequency_file_multiple.csv')
        list_of_satellites = Satellite.from_tle_file(tlefilepath=tle_file)
        frequency_list = GetFrequencyDataFromCsv(filepath=frequency_file).get()
        list_of_satellites_with_frequency = [
            replace(satellite, frequency=frequency_list.get(satellite.tle_information.satellite_number, []))
            for satellite in list_of_satellites]
        reservation = Reservation(facility=Facility(elevation=0, coordinates=Coordinates(latitude=40.8178049, longitude=-121.4695413), name='name', azimuth=30),
                                  time=TimeWindow(begin=datetime(year=2023, month=2, day=22, hour=1, tzinfo=pytz.utc), end=datetime(year=2023, month=2, day=22, hour=2, tzinfo=pytz.utc)),
                                  frequency=FrequencyRange(
                                      frequency=None,
                                      bandwidth=None
                                  )
                                  )
        overhead_windows = EventFinderRhodesMill(list_of_satellites=list_of_satellites_with_frequency,
                                                 reservation=reservation,
                                                 antenna_direction_path=[]).get_overhead_windows()
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
                frequency=[]
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
                frequency=[]
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
