from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from satellite_determination.dataclasses.coordinates import Coordinates
from satellite_determination.dataclasses.facility import Facility
from satellite_determination.dataclasses.reservation import Reservation
from satellite_determination.retrievers.satellite_retriever.satellite_retriever import SatelliteRetriever
from satellite_determination.retrievers.satellite_retriever.satellite_retriever_json_file import \
    SatelliteRetrieverJsonFile
from tests.utilities import get_script_directory
from tests.window_finder import satellite_jsons


class WindowFinder:
    def __init__(self,
                 ideal_reservation: Reservation,
                 satellites: SatelliteRetriever,
                 search_window: timedelta = timedelta(weeks=1),
                 start_time_increments: timedelta = timedelta(minutes=15)):
        self._ideal_reservation = ideal_reservation
        self._satellite_retriever = satellite_retriever
        self._search_window = search_window
        self._start_time_increments = start_time_increments

    def find(self) -> List[datetime]:
        return self._potential_start_times

    @property
    def _potential_start_times(self) -> List[datetime]:
        number_of_slots = int(self._search_window.total_seconds() / self._start_time_increments.total_seconds())
        return [self._get_time_slot(i) for i in range(1, number_of_slots + 1)]

    def _get_time_slot(self, index: int) -> datetime:
        backwards_forwards = (-1) ** index
        multiplier = int(index / 2)
        return self._ideal_reservation.time_start + backwards_forwards * self._start_time_increments * multiplier


class TestWindowFinder:
    def test_times_returned_sorted_by_closest_to_ideal_reservation(self):
        suggestions = WindowFinder(
            ideal_reservation=self._reservation,
            satellite_retriever=self._satellite_retriever(json_filename='satellites_empty.json'),
            start_time_increments=timedelta(days=1)
        ).find()
        expected_suggestions = [
            datetime(year=2022, month=11, day=20),
            datetime(year=2022, month=11, day=21),
            datetime(year=2022, month=11, day=19),
            datetime(year=2022, month=11, day=22),
            datetime(year=2022, month=11, day=18),
            datetime(year=2022, month=11, day=23),
            datetime(year=2022, month=11, day=17)
        ]
        assert suggestions == expected_suggestions

    def test_times_sorted_by_least_number_of_satellites(self):
        suggestions = WindowFinder(
            ideal_reservation=self._reservation,
            satellite_retriever=self._satellite_retriever(json_filename='satellites_empty.json'),
            start_time_increments=timedelta(days=1)
        ).find()
        expected_suggestions = [
            datetime(year=2022, month=11, day=20),
            datetime(year=2022, month=11, day=21),
            datetime(year=2022, month=11, day=19),
            datetime(year=2022, month=11, day=22),
            datetime(year=2022, month=11, day=18),
            datetime(year=2022, month=11, day=23),
            datetime(year=2022, month=11, day=17)
        ]
        assert suggestions == expected_suggestions

    @property
    def _reservation(self) -> Reservation:
        return Reservation(
            facility=Facility(
                angle_of_visibility_cone=1.,
                point_coordinates=Coordinates(latitude=1., longitude=2.),
                name='name'
            ),
            time_start=datetime(year=2022, month=11, day=20),
            time_end=datetime(year=2022, month=11, day=21))

    def _satellite_retriever(self, json_filename: str) -> SatelliteRetriever:
        return SatelliteRetrieverJsonFile(
            filepath=Path(get_script_directory(satellite_jsons.__file__), json_filename))
