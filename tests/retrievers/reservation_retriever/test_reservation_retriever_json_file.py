from datetime import datetime
from typing import List

from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.retrievers.reservation_retriever.reservation_retriever_json_file import \
    ReservationRetrieverJsonFile
from tests.retrievers.retriever_json_file_tester import RetrieverJsonFileTester


class TestReservationRetrieverJsonFile:
    def test_can_retrieve_from_json_file(self):
        assert RetrieverJsonFileTester(__file__,
                                       expected_list=self._expected_reservations,
                                       retriever_class=ReservationRetrieverJsonFile,
                                       json_filename='reservations.json').can_retrieve_from_json_file()

    @property
    def _expected_reservations(self) -> List[Reservation]:
        return [
            Reservation(
                facility=Facility(
                    elevation=45.,
                    point_coordinates=Coordinates(latitude=1., longitude=2.),
                    name='ArbitraryFacilityName1',
                    azimuth=30
                ),
                time=TimeWindow(
                    begin=datetime(year=2022, month=3, day=30, hour=16),
                    end=datetime(year=2022, month=3, day=30, hour=17)
                )
            ),
            Reservation(
                facility=Facility(
                    elevation=20.1,
                    point_coordinates=Coordinates(latitude=4., longitude=5.),
                    name='ArbitraryFacilityName2',
                    azimuth=0
                ),
                time=TimeWindow(
                    begin=datetime(year=1994, month=7, day=16, hour=3),
                    end=datetime(year=1994, month=7, day=18, hour=2)
                )
            )
        ]
