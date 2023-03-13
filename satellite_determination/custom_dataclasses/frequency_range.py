from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from pathlib import Path
import csv
#from satellite_determination.custom_dataclasses.satellite.satellite import Satellite


class FrequencyRangeJsonKey(Enum):
    high_in_megahertz = 'high_in_megahertz'
    low_in_megahertz = 'low_in_megahertz'


@dataclass
class FrequencyRange:
    frequency: float
    bandwidth: Optional[float]

    @classmethod
    def from_csv(cls, filepath: Path, id: str) -> List['FrequencyRange']:
        frequencies = []
        with open(filepath, 'r') as file:
            frequency_file = csv.DictReader(file, fieldnames=['ID', 'Name', 'Frequency', 'Status', 'Description', 'Bandwidth'])
            data = list(frequency_file)
            for line in data:
                if line["ID"] == id:
                    if (line["Bandwidth"] == None) or (line["Bandwidth"] == ''):
                        frequency = line["Frequency"]
                        frequencies.append(FrequencyRange(float(frequency), bandwidth=None))
                    else:
                        frequency = line["Frequency"]
                        bandwidth = line["Bandwidth"]
                        frequencies.append(FrequencyRange(frequency=float(frequency), bandwidth=float(bandwidth)))
        print(frequencies)
        return frequencies
