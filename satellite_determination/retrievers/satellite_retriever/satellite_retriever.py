from typing import List

from satellite_determination.dataclasses.satellite.satellite import Satellite
from satellite_determination.retrievers.retriever import Retriever


class SatelliteRetriever(Retriever):
    def retrieve(self) -> List[Satellite]:
        pass
