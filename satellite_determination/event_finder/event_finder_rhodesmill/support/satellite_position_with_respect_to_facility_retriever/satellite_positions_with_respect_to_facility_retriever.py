from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.position_time import PositionTime


class SatellitePositionsWithRespectToFacilityRetriever(ABC):
    def __init__(self, facility: Facility, datetimes: List[datetime]):
        self._datetimes = datetimes
        self._facility_latlon = self._calculate_facility_latlon(facility)

    @abstractmethod
    def run(self) -> PositionTime:
        pass

    @abstractmethod
    def _calculate_facility_latlon(self, facility: Facility):
        pass
