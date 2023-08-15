from dataclasses import replace
from typing import List

from satellite_determination.custom_dataclasses.frequency_range.support.get_frequency_data_from_csv import \
    GetFrequencyDataFromCsv
from satellite_determination.utilities import get_frequencies_filepath, get_satellites_filepath
from satellite_determination.path_finder.observation_path_finder import ObservationPathFinder
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.configuration import Configuration
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.configuration_loader.configuration_loader import ConfigurationLoader

class ConfigurationLoaderConfigFile(ConfigurationLoader):
    def __init__(self, config_file: Configuration):
        self.config = config_file

    def get_reservation(self) -> Reservation:
        return self.config.reservation

    def get_satellite_list(self, tle_file, frequency_file) -> List[Satellite]:
        satellite_list = Satellite.from_tle_file(tlefilepath=tle_file)
        frequency_list = GetFrequencyDataFromCsv(filepath=frequency_file).get()

        satellite_list_with_frequencies = [replace(satellite, frequency=frequency_list.get(satellite.tle_information.satellite_number, []))
                                           for satellite in satellite_list]

        return satellite_list_with_frequencies

    def get_antenna_direction_path(self):
        if self.config.antenna_position_times:
            return self.config.antenna_position_times
        elif self.config.static_antenna_position:
            return [PositionTime(position=self.config.static_antenna_position,
                                 time=self.config.reservation.time.begin)]
        else:
            return ObservationPathFinder(facility=self.config.reservation.facility,
                                         observation_target=self.config.observation_target,
                                         time_window=self.config.reservation.time).calculate_path()
