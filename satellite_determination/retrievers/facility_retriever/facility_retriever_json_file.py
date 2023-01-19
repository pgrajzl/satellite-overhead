from typing import List

from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.retrievers.facility_retriever.facility_retriever import FacilityRetriever
from satellite_determination.retrievers.retriever_json_file import RetrieverJsonFile

FACILITIES_JSON_KEY = 'facilities'


class FacilityRetrieverJsonFile(FacilityRetriever, RetrieverJsonFile):
    def retrieve(self) -> List[Facility]:
        return [Facility.from_json(info) for info in self._json[FACILITIES_JSON_KEY]]
