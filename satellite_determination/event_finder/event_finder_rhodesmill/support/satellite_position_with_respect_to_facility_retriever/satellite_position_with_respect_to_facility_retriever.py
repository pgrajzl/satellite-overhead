from abc import ABC, abstractmethod
from datetime import datetime

from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite


class SatellitePositionWithRespectToFacilityRetriever(ABC):
    def __init__(self, satellite: Satellite, timestamp: datetime, facility: Facility):
        self._satellite = satellite
        self._timestamp = timestamp
        self._facility = facility

    @abstractmethod
    def run(self) -> PositionTime:
        pass
