from dataclasses import dataclass
from typing import Optional


@dataclass
class FrequencyRange:
    frequency: Optional[float] = None
    bandwidth: Optional[float] = None
    status: Optional[str] = None

    def overlaps(self, satellite_frequency: 'FrequencyRange'):
        half_bandwidth_res = self.bandwidth/2
        default_bandwidth = 10
        if satellite_frequency.bandwidth is None:
            low_in_mghz_sat = satellite_frequency.frequency - (default_bandwidth/2)
            high_in_mghz_sat = satellite_frequency.frequency + (default_bandwidth/2)
            low_in_mghz_res = self.frequency - half_bandwidth_res
            high_in_mghz_res = self.frequency + half_bandwidth_res
        else:
            half_bandwidth_sat = satellite_frequency.bandwidth / 2
            low_in_mghz_res = self.frequency - half_bandwidth_res
            high_in_mghz_res = self.frequency + half_bandwidth_res
            low_in_mghz_sat = satellite_frequency.frequency - half_bandwidth_sat
            high_in_mghz_sat = satellite_frequency.frequency + half_bandwidth_sat
        return (low_in_mghz_res <= low_in_mghz_sat <= high_in_mghz_res) or \
            (high_in_mghz_res >= high_in_mghz_sat >= low_in_mghz_res) or \
            (low_in_mghz_sat <= low_in_mghz_res and high_in_mghz_sat>= high_in_mghz_res)
