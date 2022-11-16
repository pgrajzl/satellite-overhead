from abc import ABC, abstractmethod
from typing import List

from satellite_determination.dataclasses.reservation import Reservation


class ReservationRetriever(ABC):
    @abstractmethod
    def retrieve(self) -> List[Reservation]:
        pass
