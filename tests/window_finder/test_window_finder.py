from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from satellite_determination.dataclasses.coordinates import Coordinates
from satellite_determination.dataclasses.facility import Facility
from satellite_determination.dataclasses.frequency_range import FrequencyRange
from satellite_determination.dataclasses.reservation import Reservation
from satellite_determination.dataclasses.satellite import Satellite
from satellite_determination.dataclasses.time_window import TimeWindow
from satellite_determination.retrievers.satellite_retriever.satellite_retriever import SatelliteRetriever
from satellite_determination.retrievers.satellite_retriever.satellite_retriever_json_file import \
    SatelliteRetrieverJsonFile
from tests.utilities import get_script_directory
from tests.window_finder import satellite_jsons


@dataclass
class OverheadWindow:
    satellite: Satellite
    overhead_time: TimeWindow


class Validator(ABC):
    @abstractmethod
    def overhead_list(self, list_of_satellites: List[Satellite], reservation: Reservation) -> List[OverheadWindow]:
        pass


class ValidatorAllSatellitesAreOverheadAtSpecificTimes(Validator):
    def __init__(self, overhead_times: List[TimeWindow]):
        self._overhead_times = overhead_times

    def overhead_list(self, list_of_satellites: List[Satellite], reservation: Reservation) -> List[OverheadWindow]:
        return [OverheadWindow(satellite=satellite, overhead_time=overhead_time)
                for satellite, overhead_time in zip(list_of_satellites, self._overhead_times)
                if overhead_time.overlaps(reservation.time)]


class WindowFinder:
    def __init__(self,
                 ideal_reservation: Reservation,
                 satellites: List[Satellite],
                 validator: Validator,
                 search_window: timedelta = timedelta(weeks=1),
                 start_time_increments: timedelta = timedelta(minutes=15)):
        self._ideal_reservation = ideal_reservation
        self._satellites = satellites
        self._search_window = search_window
        self._start_time_increments = start_time_increments
        self._validator = validator

    def find(self) -> List[datetime]:
        potential_time_windows = [TimeWindow(begin=start_time, end=start_time + self._ideal_reservation.time.duration)
                                  for start_time in self._potential_start_times]
        potential_reservations = [Reservation(facility=self._ideal_reservation.facility, time=time) for time in potential_time_windows]
        reservations_sorted_by_number_of_overhead_satellites =\
            sorted(potential_reservations, key=lambda reservation: len(self._satellites_overhead(reservation=reservation)))
        return [reservation.time.begin for reservation in reservations_sorted_by_number_of_overhead_satellites]

    def _satellites_overhead(self, reservation: Reservation) -> List[OverheadWindow]:
        return self._validator.overhead_list(list_of_satellites=self._satellites,
                                             reservation=reservation)

    @property
    def _potential_start_times(self) -> List[datetime]:
        number_of_slots = int(self._search_window.total_seconds() / self._start_time_increments.total_seconds())
        return [self._get_time_slot(i) for i in range(1, number_of_slots + 1)]

    def _get_time_slot(self, index: int) -> datetime:
        backwards_forwards = (-1) ** index
        multiplier = int(index / 2)
        return self._ideal_reservation.time.begin + backwards_forwards * self._start_time_increments * multiplier


class TestWindowFinder:
    def test_times_returned_sorted_by_closest_to_ideal_reservation(self):
        suggestions = WindowFinder(
            ideal_reservation=self._reservation,
            satellites=[],
            validator=ValidatorAllSatellitesAreOverheadAtSpecificTimes(overhead_times=[]),
            start_time_increments=timedelta(days=1),
            search_window=timedelta(weeks=1)
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
        arbitrary_frequency_range = FrequencyRange(high_in_megahertz=2., low_in_megahertz=1.)
        arbitrary_satellite_number = 'satellite_number'
        overhead_windows = [
            OverheadWindow(satellite=Satellite(frequency=arbitrary_frequency_range,
                                               satellite_number=arbitrary_satellite_number,
                                               name='name1'),
                           overhead_time=TimeWindow(begin=datetime(year=2022, month=11, day=20),
                                                    end=datetime(year=2022, month=11, day=20, hour=1))),
            OverheadWindow(satellite=Satellite(frequency=arbitrary_frequency_range,
                                               satellite_number=arbitrary_satellite_number,
                                               name='name2'),
                           overhead_time=TimeWindow(begin=datetime(year=2022, month=11, day=20),
                                                    end=datetime(year=2022, month=11, day=20, hour=1))),
            OverheadWindow(satellite=Satellite(frequency=arbitrary_frequency_range,
                                               satellite_number=arbitrary_satellite_number,
                                               name='name3'),
                           overhead_time=TimeWindow(begin=datetime(year=2022, month=11, day=21),
                                                    end=datetime(year=2022, month=11, day=21, hour=1))),
            ]

        suggestions = WindowFinder(
            ideal_reservation=self._reservation,
            satellites=[window.satellite for window in overhead_windows],
            validator=ValidatorAllSatellitesAreOverheadAtSpecificTimes(overhead_times=[window.overhead_time for window in overhead_windows]),
            start_time_increments=timedelta(days=1),
            search_window=timedelta(weeks=1)
        ).find()

        expected_suggestions = [
            datetime(year=2022, month=11, day=19),
            datetime(year=2022, month=11, day=22),
            datetime(year=2022, month=11, day=18),
            datetime(year=2022, month=11, day=23),
            datetime(year=2022, month=11, day=17),
            datetime(year=2022, month=11, day=21),
            datetime(year=2022, month=11, day=20)
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
            time=TimeWindow(begin=datetime(year=2022, month=11, day=20), end=datetime(year=2022, month=11, day=21)))

    def _satellite_retriever(self, json_filename: str) -> SatelliteRetriever:
        return SatelliteRetrieverJsonFile(
            filepath=Path(get_script_directory(satellite_jsons.__file__), json_filename))
