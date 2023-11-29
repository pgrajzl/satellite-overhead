from abc import ABC, abstractmethod
from datetime import datetime

from sopp.custom_dataclasses.facility import Facility
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.custom_dataclasses.satellite.satellite import Satellite


class SatellitePositionWithRespectToFacilityRetriever(ABC):
    def __init__(self, satellite: Satellite, timestamp: datetime, facility: Facility):
        self._satellite = satellite
        self._timestamp = timestamp
        self._facility = facility

    @abstractmethod
    def run(self) -> PositionTime:
        pass
