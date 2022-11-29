from abc import ABC, abstractmethod
from typing import List

from satellite_determination.dataclasses.reservation import Reservation
from satellite_determination.retrievers.retriever import Retriever


class ReservationRetriever(Retriever, ABC):
    @abstractmethod
    def retrieve(self) -> List[Reservation]:
        pass
