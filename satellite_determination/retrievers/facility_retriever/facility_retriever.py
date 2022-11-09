from abc import ABC, abstractmethod
from typing import List

from satellite_determination.dataclasses.facility import Facility
from satellite_determination.retrievers.retriever import Retriever


class FacilityRetriever(Retriever, ABC):
    @abstractmethod
    def retrieve(self) -> List[Facility]:
        pass
