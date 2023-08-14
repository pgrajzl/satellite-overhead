from dataclasses import replace
from typing import List

from satellite_determination.custom_dataclasses.frequency_range.support.get_frequency_data_from_csv import \
    GetFrequencyDataFromCsv
from satellite_determination.utilities import get_frequencies_filepath, get_satellites_filepath
from satellite_determination.path_finder.observation_path_finder import ObservationPathFinder
from satellite_determination.config_file.support.config_file_base import ConfigFileBase
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.configuration_loader.configuration_loader import ConfigurationLoader

class ConfigurationLoaderConfigFile(ConfigurationLoader):
    def __init__(self, config_file: ConfigFileBase):
        self.config_file = config_file

    def get_reservation(self) -> Reservation:
        return self.config_file.configuration.reservation

    def get_satellite_list(self, tle_file, frequency_file) -> List[Satellite]:
        satellite_list = Satellite.from_tle_file(tlefilepath=tle_file)
        frequency_list = GetFrequencyDataFromCsv(filepath=frequency_file).get()

        satellite_list_with_frequencies = [replace(satellite, frequency=frequency_list.get(satellite.tle_information.satellite_number, []))
                                           for satellite in satellite_list]

        return satellite_list_with_frequencies

    def get_antenna_direction_path(self):
        antenna_direction_path = [PositionTime(position=self.config_file.configuration.static_antenna_position,
                                               time=self.config_file.configuration.reservation.time.begin)] \
            if self.config_file.configuration.static_antenna_position \
            else ObservationPathFinder(facility=self.config_file.configuration.reservation.facility,
                                       observation_target=self.config_file.configuration.observation_target,
                                       time_window=self.config_file.configuration.reservation.time).calculate_path()
    
        return antenna_direction_path
