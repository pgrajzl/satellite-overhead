from pathlib import Path
from typing import List

from satellite_determination.dataclasses.coordinates import Coordinates
from satellite_determination.dataclasses.facility import Facility
from satellite_determination.retrievers.facility_retriever.facility_retriever_json_file import FacilityRetrieverJsonFile
from tests.utilities import get_script_directory


class TestFacilityRetrieverJsonFile:
    def test_can_retrieve_from_json_file(self):
        retriever = FacilityRetrieverJsonFile(filepath=self._reservations_filepath)
        facilities = retriever.retrieve()
        assert facilities == self._expected_facilities

    @property
    def _reservations_filepath(self) -> Path:
        facilities_directory = get_script_directory(__file__)
        reservations_filepath = Path(facilities_directory, 'facilities.json')
        return reservations_filepath

    @property
    def _expected_facilities(self) -> List[Facility]:
        return [
            Facility(
                angle_of_visibility_cone=45.,
                point_coordinates=Coordinates(latitude=1., longitude=2.),
                name='ArbitraryFacilityName1'
            ),
            Facility(
                angle_of_visibility_cone=20.1,
                point_coordinates=Coordinates(latitude=4., longitude=5.),
                name='ArbitraryFacilityName2'
            )
        ]
