from abc import ABC, abstractmethod
from typing import List

from satellite_determination.custom_dataclasses.observation_path import ObservationPath
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite


class EventFinder(ABC):
    def __init__(self, list_of_satellites: List[Satellite], reservation: Reservation, azimuth_altitude_path: List[ObservationPath]):
        self._list_of_satellites = list_of_satellites
        self._reservation = reservation
        self._path = azimuth_altitude_path

    @abstractmethod
    def get_overhead_windows(self) -> List[OverheadWindow]:
        pass

    @abstractmethod
    def get_overhead_windows_slew(self) -> List[OverheadWindow]:
        pass
