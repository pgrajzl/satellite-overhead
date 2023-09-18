from dataclasses import replace
from typing import List
from functools import cached_property

from satellite_determination.satellites_loader.satellites_loader import SatellitesLoader
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.frequency_range.support.get_frequency_data_from_csv import \
    GetFrequencyDataFromCsv


class SatellitesLoaderFromFiles(SatellitesLoader):
    """
    A class for loading satellite information from TLE (Two-Line Element) and a frequency data file.

    This class extends the `SatellitesLoader` class to provide functionality for loading satellite
    information from TLE files and optionally associating frequency data with the satellites.

    Example usage:

    >>> loader = SatellitesLoaderFromFiles(tle_file='satellite_data.tle', frequency_file='frequency_data.csv')
    >>> satellites = loader.load_satellites()
    >>> for satellite in satellites:
    >>>     print(satellite)
    """

    def __init__(self, tle_file, frequency_file=None):
        self.tle_file = tle_file
        self.frequency_file = frequency_file

    def load_satellites(self) -> List[Satellite]:
        if self._satellites_freq_data is not None:
            satellite_list_with_frequencies = [
                replace(
                    satellite,
                    frequency=self._satellites_freq_data.get(satellite.tle_information.satellite_number, [])
                )
                for satellite in self._satellites_from_tle
            ]

            return satellite_list_with_frequencies

        return self._satellites_from_tle

    @cached_property
    def _satellites_from_tle(self):
        return Satellite.from_tle_file(tlefilepath=self.tle_file)

    @cached_property
    def _satellites_freq_data(self):
        if self.frequency_file is not None:
            return GetFrequencyDataFromCsv(filepath=self.frequency_file).get()
        else:
            return None
