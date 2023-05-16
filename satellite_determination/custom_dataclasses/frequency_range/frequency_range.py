from dataclasses import dataclass
from typing import Optional

'''
The FrequencyRange class is used for storing frequency ranges of both the RA telescopes observation and each satellite's downlink transmission
frequency information. The frequency parameter represents the center frequency of the observation or downlink. The status parameter is only relevant
to satellites and is used to store information from the satellite frequency database on whether an antenna is operational 'active' or not 'inactive'

The overlaps function determines if two FrequencyRanges overlap with each other and is used to determine if any of the satellite downlink frequencies
overlap with the observation frequency. Satellite frequency data is read from a csv file (as of May 15, 2023) using the GetFrequencyDataFromCsv class
under the support folder.f

'''

DEFAULT_BANDWIDTH = 10

@dataclass
class FrequencyRange:
    frequency: Optional[float] = None
    bandwidth: Optional[float] = None
    status: Optional[str] = None

    def overlaps(self, satellite_frequency: 'FrequencyRange'):
        half_bandwidth_res = self.bandwidth/2
        if satellite_frequency.bandwidth is None:
            low_in_mghz_sat = satellite_frequency.frequency - (DEFAULT_BANDWIDTH/2)
            high_in_mghz_sat = satellite_frequency.frequency + (DEFAULT_BANDWIDTH/2)
            low_in_mghz_res = self.frequency - half_bandwidth_res
            high_in_mghz_res = self.frequency + half_bandwidth_res
        else:
            half_bandwidth_sat = satellite_frequency.bandwidth / 2
            low_in_mghz_res = self.frequency - half_bandwidth_res
            high_in_mghz_res = self.frequency + half_bandwidth_res
            low_in_mghz_sat = satellite_frequency.frequency - half_bandwidth_sat
            high_in_mghz_sat = satellite_frequency.frequency + half_bandwidth_sat
        return low_in_mghz_sat < high_in_mghz_res and high_in_mghz_sat > low_in_mghz_res
