from typing import List

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.retrievers.facility_retriever.facility_retriever_json_file import FacilityRetrieverJsonFile
from tests.retrievers.retriever_json_file_tester import RetrieverJsonFileTester


class TestFacilityRetrieverJsonFile:
    def test_can_retrieve_from_json_file(self):
        assert RetrieverJsonFileTester(__file__,
                                       expected_list=self._expected_facilities,
                                       retriever_class=FacilityRetrieverJsonFile,
                                       json_filename='facilities.json').can_retrieve_from_json_file()

    @property
    def _expected_facilities(self) -> List[Facility]:
        return [
            Facility(
                angle_of_visibility_cone=45.,
                point_coordinates=Coordinates(latitude=1., longitude=2.),
                name='ArbitraryFacilityName1',
                azimuth=30
            ),
            Facility(
                angle_of_visibility_cone=20.1,
                point_coordinates=Coordinates(latitude=4., longitude=5.),
                name='ArbitraryFacilityName2',
                azimuth=0
            )
        ]
