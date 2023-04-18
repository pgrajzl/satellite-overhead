from typing import List

from satellite_determination.custom_dataclasses.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite


class FrequencyFilter:

    def __init__(self, satellites: List[Satellite], observation_frequency: FrequencyRange):
        self._list_satellites = satellites
        self._observation_frequency = observation_frequency
    def filter_frequencies(self) -> List[Satellite]:
        frequency_filtered_satellite_list = []
        for sat in self._list_satellites:
            for sat_frequency in sat.frequency:
                if sat_frequency.frequency is None or sat_frequency.frequency == '': #if we don't have a frequency for a satellite we default to assuming it could interfere
                    frequency_filtered_satellite_list.append(sat)
                    break
                if sat_frequency.status == 'active' or sat_frequency.status is None:
                    if self._observation_frequency.overlaps(sat_frequency):
                        frequency_filtered_satellite_list.append(sat)
                        break # we only need to put satellite on list once, even if multiple of its frequencies overlap
        return frequency_filtered_satellite_list
