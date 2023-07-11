from abc import ABC, abstractmethod
from datetime import timedelta
from typing import List, Type

from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellite_position_with_respect_to_facility_retriever.satellite_position_with_respect_to_facility_retriever import \
    SatellitePositionWithRespectToFacilityRetriever


class EventFinder(ABC):
    '''
    The EventFinder is the module that determines if a satellite interferes with an RA observation. It has three functions:

      + get_overhead_windows_slew():    determines if a satellite crosses the telescope's main beam as the telescope moves across the sky
                                        by looking for intersections of azimuth and altitude and returning a list of OverheadWindows for
                                        events where this occurs
      + get_overhead_windows():         Determines the satellites visible above the horizon during the search window and returns a list of
                                        OverheadWindows for each event. This can be used to find all satellite visible over the horizon or
                                        to determine events for a stationary observation if an azimuth and altitude is provided

    '''
    def __init__(self,
                 antenna_direction_path: List[PositionTime],
                 list_of_satellites: List[Satellite],
                 reservation: Reservation,
                 satellite_position_with_respect_to_facility_retriever_class: Type[SatellitePositionWithRespectToFacilityRetriever],
                 time_continuity_resolution: timedelta = timedelta(seconds=1)):
        self.antenna_direction_path = antenna_direction_path
        self.list_of_satellites = list_of_satellites
        self.reservation = reservation
        self.satellite_position_with_respect_to_facility_retriever_class = satellite_position_with_respect_to_facility_retriever_class
        self.time_continuity_resolution = time_continuity_resolution

    @abstractmethod
    def get_satellites_above_horizon(self) -> List[OverheadWindow]:
        pass

    @abstractmethod
    def get_satellites_crossing_main_beam(self) -> List[OverheadWindow]:
        pass
