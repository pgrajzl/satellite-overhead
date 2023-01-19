from typing import List

from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.retrievers.retriever_json_file import RetrieverJsonFile
from satellite_determination.retrievers.satellite_retriever.satellite_retriever import SatelliteRetriever

SATELLITES_JSON_KEY = 'satellites'


class SatelliteRetrieverJsonFile(SatelliteRetriever, RetrieverJsonFile):
    def retrieve(self) -> List[Satellite]:
        return [Satellite.from_json(info) for info in self._json[SATELLITES_JSON_KEY]]
