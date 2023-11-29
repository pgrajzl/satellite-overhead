from typing import List

from sopp.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from sopp.custom_dataclasses.satellite.satellite import Satellite

'''
The FrequencyFilter determines if a satellite's downlink transmission frequency overlaps with the desired observation frequency
and returns a list of Satellite objects that contains only the satellites that will potentially interfere with the observation.
If there is no information on the satellite frequency, it will include the satellite in the list to err on the side of caution
for potential interference.

'''
class FrequencyFilter:

    def __init__(self, satellites: List[Satellite], observation_frequency: FrequencyRange):
        self._list_satellites = satellites
        self._observation_frequency = observation_frequency

    def filter_frequencies(self) -> List[Satellite]:
        frequency_filtered_satellite_list = []

        for sat in self._list_satellites:
            has_missing_frequency = not sat.frequency or any(sf.frequency is None for sf in sat.frequency)

            frequency_overlaps_target_frequency = not has_missing_frequency and any(
                sf.status != 'inactive' and self._observation_frequency.overlaps(sf)
                for sf in sat.frequency
            )

            if has_missing_frequency or frequency_overlaps_target_frequency:
                frequency_filtered_satellite_list.append(sat)

        return frequency_filtered_satellite_list
