import json
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

from tests.utilities import get_script_directory


@dataclass
class Coordinates:
    latitude: float
    longitude: float

    @classmethod
    def from_json(cls, info: dict) -> 'Coordinates':
        return Coordinates(
            latitude=info['latitude'],
            longitude=info['longitude']
        )


@dataclass
class Facility:
    angle_of_visibility_cone: float
    point_coordinates: Coordinates
    name: str

    @classmethod
    def from_json(cls, info: dict) -> 'Facility':
        return Facility(
            angle_of_visibility_cone=info['angle_of_visibility_cone'],
            point_coordinates=Coordinates.from_json(info['point_coordinates']),
            name=info['name']
        )


@dataclass
class Reservation:
    facility: Facility
    time_start: datetime
    time_end: datetime

    @classmethod
    def from_json(cls, info: dict) -> 'Reservation':
        return Reservation(
            facility=Facility.from_json(info['facility']),
            time_start=datetime.fromisoformat(info['time_start']),
            time_end=datetime.fromisoformat(info['time_end'])
        )


class ReservationRetriever(ABC):
    def retrieve(self) -> List[Reservation]:
        pass


class ReservationRetrieverJsonFile(ReservationRetriever):
    def __init__(self, filepath: Path):
        self._filepath = filepath

    def retrieve(self) -> List[Reservation]:
        return [Reservation.from_json(info) for info in self._reservations_json['reservations']]

    @property
    def _reservations_json(self) -> dict:
        with open(self._filepath, 'r') as f:
            return json.load(f)


class TestReservationRetriever:
    def test(self):
        reservations_directory = get_script_directory(__file__)
        reservations_filepath = Path(reservations_directory, 'reservations.json')
        retriever = ReservationRetrieverJsonFile(filepath=reservations_filepath)
        reservations = retriever.retrieve()
        assert reservations == [
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
                    name='ArbitraryFacilityName1'
                ),
                time_start=datetime(year=1994, month=7, day=16, hour=3),
                time_end=datetime(year=2022, month=7, day=18, hour=2)
            ),
        ]

