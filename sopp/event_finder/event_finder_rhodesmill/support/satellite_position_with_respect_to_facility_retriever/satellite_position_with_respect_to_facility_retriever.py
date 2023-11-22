from abc import ABC, abstractmethod
from datetime import datetime

from sopp.dataclasses.facility import Facility
from sopp.dataclasses.position_time import PositionTime
from sopp.dataclasses.satellite.satellite import Satellite


class SatellitePositionWithRespectToFacilityRetriever(ABC):
    def __init__(self, satellite: Satellite, timestamp: datetime, facility: Facility):
        self._satellite = satellite
        self._timestamp = timestamp
        self._facility = facility

    @abstractmethod
    def run(self) -> PositionTime:
        pass
