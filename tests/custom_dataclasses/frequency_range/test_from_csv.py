from satellite_determination.custom_dataclasses.frequency_range import FrequencyRange
from tests.utilities import get_script_directory
from pathlib import Path

class TestFromCsv:

    def test_one_frequency(self):
        frequency_file = Path(get_script_directory(__file__), 'arbitrary_frequency_file.csv')
        frequencies = FrequencyRange.from_csv(filepath=frequency_file, id='2023')
        assert frequencies == [
            FrequencyRange(
                frequency=136.65,
                bandwidth=None
            )
        ]

    def test_two_frequencies(self):
        frequency_file = Path(get_script_directory(__file__), 'arbitrary_frequency_file_two_frequencies.csv')
        frequencies = FrequencyRange.from_csv(filepath=frequency_file, id='2023')
        assert frequencies == [
            FrequencyRange(
                frequency=136.65,
                bandwidth=None
            ),
            FrequencyRange(
                frequency=2,
                bandwidth=None
            )
        ]

    def test_with_bandwidth(self):
        frequency_file = Path(get_script_directory(__file__), 'arbitrary_frequency_file_with_bandwidth.csv')
        frequencies = FrequencyRange.from_csv(filepath=frequency_file, id='2023')
        assert frequencies == [
            FrequencyRange(
                frequency=136.65,
                bandwidth=None
            ),
            FrequencyRange(
                frequency=2,
                bandwidth=None
            ),
            FrequencyRange(
                frequency=500,
                bandwidth=200
            )
        ]


