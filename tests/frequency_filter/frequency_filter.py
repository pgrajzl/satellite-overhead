from typing import List
from satellite_determination.custom_dataclasses.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite

class FrequencyFilter:

    def __init__(self, satellites: List[Satellite], observation_frequency: FrequencyRange):
        self._list_satellites = satellites
        self._observation_frequency = observation_frequency
    def get_frequencies(self) -> List[Satellite]:
        frequency_filtered_satellite_list = []
        for sat in self._list_satellites:
            for frequency in sat.frequency:
                if ((frequency < (self._observation_frequency.frequency + (self._observation_frequency.bandwidth/2))) and (frequency > (self._observation_frequency.frequency - (self._observation_frequency.bandwidth/2)))):
                    frequency_filtered_satellite_list.append(sat)
        return frequency_filtered_satellite_list

