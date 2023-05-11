from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from pathlib import Path
import csv

@dataclass
class FrequencyRange:
    frequency: Optional[float] = None
    bandwidth: Optional[float] = None
    status: Optional[str] = None

    @classmethod
    def from_csv(cls, filepath: Path, satcat_id: int) -> List['FrequencyRange']:
        frequencies = []
        with open(filepath, 'r') as file:
            frequency_file = csv.DictReader(file, fieldnames=['ID', 'Name', 'Frequency', 'Status', 'Description', 'Bandwidth'])
            data = list(frequency_file)
            for line in data:
                if line["ID"] == str(satcat_id):
                    if (line["Frequency"] is None) or (line["Frequency"] == 'None'):
                        status = line["Status"]
                        frequencies.append(FrequencyRange(frequency=None, bandwidth=None, status=status))
                    elif (line["Bandwidth"] is None) or (line["Bandwidth"] == ''):
                        frequency = line["Frequency"]
                        status = line["Status"]
                        frequencies.append(FrequencyRange(float(frequency), bandwidth=None, status=status))
                    else:
                        frequency = line["Frequency"]
                        bandwidth = line["Bandwidth"]
                        status = line["Status"]
                        frequencies.append(FrequencyRange(frequency=float(frequency), bandwidth=float(bandwidth), status=status))
            if len(frequencies) == 0:
                frequencies.append(FrequencyRange(frequency=None, bandwidth=None, status=None))
        return frequencies

    def overlaps(self, satellite_frequency: 'FrequencyRange'):
        if satellite_frequency.bandwidth is None:
            low_in_mghz_sat = satellite_frequency.frequency - 5 #TODO get rid of magic number
            high_in_mghz_sat = satellite_frequency.frequency + 5
            low_in_mghz_res = self.frequency - (self.bandwidth / 2)
            high_in_mghz_res = self.frequency + (self.bandwidth / 2)
        else:
            low_in_mghz_res = self.frequency - (self.bandwidth/2)
            high_in_mghz_res = self.frequency + (self.bandwidth / 2)
            low_in_mghz_sat = satellite_frequency.frequency - (satellite_frequency.bandwidth/2)
            high_in_mghz_sat = satellite_frequency.frequency + (satellite_frequency.bandwidth/2)
        return (low_in_mghz_res <= low_in_mghz_sat <= high_in_mghz_res) or \
            (high_in_mghz_res >= high_in_mghz_sat >= low_in_mghz_res) or \
            (low_in_mghz_sat <= low_in_mghz_res and high_in_mghz_sat>= high_in_mghz_res)
