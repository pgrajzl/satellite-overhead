from pathlib import Path
from typing import Type

from satellite_determination.retrievers.retriever_json_file import RetrieverJsonFile
from tests.utilities import get_script_directory


class RetrieverJsonFileTester:
    def __init__(self, module, expected_list: list, retriever_class: Type[RetrieverJsonFile], json_filename: str):
        self._expected_list = expected_list
        self._module = module
        self._retriever_class = retriever_class
        self._json_filename = json_filename

    def can_retrieve_from_json_file(self):
        retriever = self._retriever_class(filepath=self._reservations_filepath)
        satellites = retriever.retrieve()
        return satellites == self._expected_list

    @property
    def _reservations_filepath(self) -> Path:
        reservations_directory = get_script_directory(self._module)
        reservations_filepath = Path(reservations_directory, self._json_filename)
        return reservations_filepath
