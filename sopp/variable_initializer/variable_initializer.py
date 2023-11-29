from abc import ABC, abstractmethod
from typing import List

from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.satellite.satellite import Satellite
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.satellites_loader.satellites_loader import SatellitesLoader

class VariableInitializer(ABC):
    def __init__(self, satellites_loader: SatellitesLoader):
        self.satellites_loader = satellites_loader

    @abstractmethod
    def get_reservation(self) -> Reservation:
        pass

    def get_satellite_list(self) -> List[Satellite]:
        return self.satellites_loader.load_satellites()

    @abstractmethod
    def get_antenna_direction_path(self) -> List[PositionTime]:
        pass
