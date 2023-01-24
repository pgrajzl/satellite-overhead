from typing import List

from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.retrievers.reservation_retriever.reservation_retriever import ReservationRetriever
from satellite_determination.retrievers.retriever_json_file import RetrieverJsonFile

RESERVATIONS_JSON_KEY = 'reservations'


class ReservationRetrieverJsonFile(ReservationRetriever, RetrieverJsonFile):
    def retrieve(self) -> List[Reservation]:
        return [Reservation.from_json(info) for info in self._json[RESERVATIONS_JSON_KEY]]
