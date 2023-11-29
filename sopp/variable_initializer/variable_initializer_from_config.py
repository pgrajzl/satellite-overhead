from dataclasses import replace
from typing import List

from sopp.path_finder.observation_path_finder_astropy import ObservationPathFinderAstropy
from sopp.custom_dataclasses.satellite.satellite import Satellite
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.configuration import Configuration
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.variable_initializer.variable_initializer import VariableInitializer
from sopp.satellites_loader.satellites_loader import SatellitesLoader

class VariableInitializerFromConfig(VariableInitializer):
    def __init__(self, config: Configuration, satellites_loader: SatellitesLoader):
        super().__init__(satellites_loader)
        self.config = config

    def get_reservation(self) -> Reservation:
        return self.config.reservation

    def get_antenna_direction_path(self) -> List[PositionTime]:
        if self.config.antenna_position_times:
            return self.config.antenna_position_times
        elif self.config.static_antenna_position:
            return [PositionTime(position=self.config.static_antenna_position,
                                 time=self.config.reservation.time.begin)]
        else:
            return ObservationPathFinderAstropy(facility=self.config.reservation.facility,
                                         observation_target=self.config.observation_target,
                                         time_window=self.config.reservation.time).calculate_path()
