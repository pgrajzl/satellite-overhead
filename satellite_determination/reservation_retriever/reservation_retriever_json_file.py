import json
from pathlib import Path
from typing import List

from satellite_determination.dataclasses.reservation import Reservation
from satellite_determination.reservation_retriever.reservation_retriever import ReservationRetriever


class ReservationRetrieverJsonFile(ReservationRetriever):
    def __init__(self, filepath: Path):
        self._filepath = filepath

    def retrieve(self) -> List[Reservation]:
        return [Reservation.from_json(info) for info in self._reservations_json['reservations']]

    @property
    def _reservations_json(self) -> dict:
        with open(self._filepath, 'r') as f:
            return json.load(f)
