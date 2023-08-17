from abc import ABC, abstractmethod
from typing import List

from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite

class ConfigurationLoader(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_reservation(self) -> Reservation:
        pass

    @abstractmethod
    def get_satellite_list(self) -> List[Satellite]:
        pass

    @abstractmethod
    def get_antenna_direction_path(self):
        pass
