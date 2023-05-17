import csv
from enum import Enum
from pathlib import Path
from typing import Dict, List

from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange


class FrequencyCsvKeys(Enum):
    ID = 'ID'
    NAME = 'Name'
    FREQUENCY = 'Frequency [MHz]'
    STATUS = 'Status'
    DESCRIPTION = 'Description'
    BANDWIDTH = 'Bandwidth [kHz]/Baud'


class GetFrequencyDataFromCsv:
    '''
    Reads frequency data from a supplied CSV. The CSV should be placed in the `supplements` folder under the name `satellite_frequencies.csv` and should be
    formatted with the following columns:
     __________________________________________________________________________________
    |   ID   |   Name   |   Frequency   |   Bandwidth   |   Status   |   Description   |

    With all values in the frequency column of the same order of magnitude (typically MHz). The same goes for bandwidth. These columns should have the
    integer value alone.


    '''
    def __init__(self, filepath: Path):
        self._filepath = filepath

    def get(self) -> Dict[int, List['FrequencyRange']]:
        frequencies = {}
        for line in self._data[1:]:
            id_string = line[FrequencyCsvKeys.ID.value]
            if not id_string or id_string == 'None':
                continue

            frequency_range = FrequencyRange(frequency=self._get_frequency(line),
                                             bandwidth=self._get_bandwidth(line),
                                             status=line[FrequencyCsvKeys.STATUS.value])
            id_int = int(id_string)
            if id_int not in frequencies:
                frequencies[id_int] = []
                # frequencies[id_int] = [FrequencyRange(frequency=None, bandwidth=None, status=None)]
            frequencies[id_int].append(frequency_range)
        return frequencies

    @staticmethod
    def _get_frequency(line: Dict[str, str]):
        frequency = line[FrequencyCsvKeys.FREQUENCY.value]
        return None if frequency is None or frequency == 'None' else float(frequency)

    @staticmethod
    def _get_bandwidth(line: Dict[str, str]):
        bandwidth = line[FrequencyCsvKeys.BANDWIDTH.value]
        return None if bandwidth is None or bandwidth == '' else float(bandwidth)

    @property
    def _data(self) -> List[Dict[str, str]]:
        with open(self._filepath, 'r') as file:
            return list(csv.DictReader(file, fieldnames=[e.value for e in FrequencyCsvKeys]))
