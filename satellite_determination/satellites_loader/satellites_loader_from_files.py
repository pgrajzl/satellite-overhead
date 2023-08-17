from dataclasses import replace
from typing import List

from satellite_determination.satellites_loader.satellites_loader import SatellitesLoader
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.frequency_range.support.get_frequency_data_from_csv import \
    GetFrequencyDataFromCsv

class SatellitesLoaderFromFiles(SatellitesLoader):
    def __init__(self, tle_file, frequency_file):
        self.tle_file = tle_file
        self.frequency_file = frequency_file

    def load_satellites(self) -> List[Satellite]:
        satellite_list = Satellite.from_tle_file(tlefilepath=self.tle_file)
        frequency_list = GetFrequencyDataFromCsv(filepath=self.frequency_file).get()

        satellite_list_with_frequencies = [replace(satellite, frequency=frequency_list.get(satellite.tle_information.satellite_number, []))
                                           for satellite in satellite_list]

        return satellite_list_with_frequencies
