from typing import List

from satellite_determination.dataclasses.frequency_range import FrequencyRange
from satellite_determination.dataclasses.satellite import Satellite
from satellite_determination.retrievers.satellite_retriever.satellite_retriever_json_file import \
    SatelliteRetrieverJsonFile
from tests.retrievers.retriever_json_file_tester import RetrieverJsonFileTester


class TestReservationRetriever:
    def test_can_retrieve_from_json_file(self):
        assert RetrieverJsonFileTester(__file__,
                                       expected_list=self._expected_satellites,
                                       retriever_class=SatelliteRetrieverJsonFile,
                                       json_filename='satellites.json').can_retrieve_from_json_file()

    @property
    def _expected_satellites(self) -> List[Satellite]:
        return [
            Satellite(
                frequency=FrequencyRange(high_in_megahertz=2., low_in_megahertz=1.),
                satellite_number='ARBITRARY1',
                name='ARBITRARY1',
            ),
            Satellite(
                frequency=FrequencyRange(high_in_megahertz=4.1, low_in_megahertz=3.),
                satellite_number='ARBITRARY2',
                name='ARBITRARY2',
            )
        ]
