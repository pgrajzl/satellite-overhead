from abc import ABC, abstractmethod
from datetime import timedelta
from typing import List, Type

from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellite_position_with_respect_to_facility_retriever.satellite_position_with_respect_to_facility_retriever import \
    SatellitePositionWithRespectToFacilityRetriever
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellite_position_with_respect_to_facility_retriever.satellite_position_with_respect_to_facility_retriever_rhodesmill import \
    SatellitePositionWithRespectToFacilityRetrieverRhodesmill


class EventFinder(ABC):
    def __init__(self,
                 list_of_satellites: List[Satellite],
                 reservation: Reservation,
                 antenna_direction_path: List[PositionTime],
                 time_continuity_resolution: timedelta = timedelta(seconds=1),
                 satellite_position_with_respect_to_facility_retriever_class: Type[SatellitePositionWithRespectToFacilityRetriever] = SatellitePositionWithRespectToFacilityRetrieverRhodesmill):
        self._antenna_direction_path = antenna_direction_path
        self._list_of_satellites = list_of_satellites
        self._reservation = reservation
        self._time_continuity_resolution = time_continuity_resolution
        self._satellite_position_with_respect_to_facility_retriever_class = satellite_position_with_respect_to_facility_retriever_class

    @abstractmethod
    def get_satellites_above_horizon(self) -> List[OverheadWindow]:
        pass

    @abstractmethod
    def get_satellites_crossing_main_beam(self) -> List[OverheadWindow]:
        pass
