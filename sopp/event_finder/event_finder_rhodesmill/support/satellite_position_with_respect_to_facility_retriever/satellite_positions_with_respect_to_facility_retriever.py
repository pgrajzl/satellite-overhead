from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from sopp.dataclasses.facility import Facility
from sopp.dataclasses.position_time import PositionTime
from sopp.dataclasses.satellite.satellite import Satellite


class SatellitePositionsWithRespectToFacilityRetriever(ABC):
    def __init__(self, facility: Facility, datetimes: List[datetime]):
        self._datetimes = datetimes
        self._facility = facility

    @abstractmethod
    def run(self, satellite: Satellite) -> List[PositionTime]:
        pass
