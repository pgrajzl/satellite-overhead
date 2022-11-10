from typing import List

from satellite_determination.dataclasses.satellite import Satellite
from satellite_determination.retrievers.retriever import Retriever
from satellite_determination.retrievers.retriever_json_file import RetrieverJsonFile

SATELLITES_JSON_KEY = 'satellites'


class SatelliteRetriever(Retriever):
    def retrieve(self) -> List[Satellite]:
        pass


class SatelliteRetrieverJsonFile(SatelliteRetriever, RetrieverJsonFile):
    def retrieve(self) -> List[Satellite]:
        return [Satellite.from_json(info) for info in self._json[SATELLITES_JSON_KEY]]
