from datetime import datetime
from pathlib import Path
from typing import List

from satellite_determination.dataclasses.reservation import Reservation
from satellite_determination.dataclasses.facility import Facility
from satellite_determination.dataclasses.coordinates import Coordinates
from satellite_determination.reservation_retriever.reservation_retriever_json_file import ReservationRetrieverJsonFile
from tests.utilities import get_script_directory


class TestReservationRetriever:
    def test_can_retrieve_from_json_file(self):
        retriever = ReservationRetrieverJsonFile(filepath=self._reservations_filepath)
        reservations = retriever.retrieve()
        assert reservations == self._expected_reservations

    @property
    def _reservations_filepath(self) -> Path:
        reservations_directory = get_script_directory(__file__)
        reservations_filepath = Path(reservations_directory, 'reservations.json')
        return reservations_filepath

    @property
    def _expected_reservations(self) -> List[Reservation]:
        return [
            Reservation(
                facility=Facility(
                    angle_of_visibility_cone=45.,
                    point_coordinates=Coordinates(latitude=1., longitude=2.),
                    name='ArbitraryFacilityName1'
                ),
                time_start=datetime(year=2022, month=3, day=30, hour=16),
                time_end=datetime(year=2022, month=3, day=30, hour=17)
            ),
            Reservation(
                facility=Facility(
                    angle_of_visibility_cone=20.1,
                    point_coordinates=Coordinates(latitude=4., longitude=5.),
                    name='ArbitraryFacilityName2'
                ),
                time_start=datetime(year=1994, month=7, day=16, hour=3),
                time_end=datetime(year=1994, month=7, day=18, hour=2)
            ),
        ]
