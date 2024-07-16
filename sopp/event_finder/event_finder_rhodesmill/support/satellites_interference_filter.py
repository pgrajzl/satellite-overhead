import itertools
from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from math import isclose
from typing import List
from abc import ABC, abstractmethod

import math

import numpy

from sopp.custom_dataclasses.facility import Facility
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.custom_dataclasses.position import Position
from sopp.custom_dataclasses.runtime_settings import RuntimeSettings

from sopp.custom_dataclasses.power_time import PowerTime
from sopp.custom_dataclasses.power_window import PowerWindow

from sopp.custom_dataclasses.antenna import Antenna

from sopp.custom_dataclasses.satellite.satellite import Satellite
from sopp.event_finder.event_finder_rhodesmill.support.satellite_positions_with_respect_to_facility_retriever.satellite_positions_with_respect_to_facility_retriever_rhodesmill import \
    SatellitePositionsWithRespectToFacilityRetrieverRhodesmill


DEGREES_IN_A_CIRCLE = 360


@dataclass
class AntennaPosition:
    satellite_positions: List[PositionTime]
    antenna_direction: PositionTime

class SatellitesFilterStrategy(ABC):
    def __init__(self, facility: Facility, runtime_settings: RuntimeSettings):
        self._facility = facility
        self._runtime_settings = runtime_settings

    @abstractmethod
    def is_in_view(self, satellite_position: Position, antenna_position: Position) -> bool:
        pass

class SatellitesInterferenceFilter:
    def __init__(
        self,
        facility: Facility,
        antenna_positions: List[AntennaPosition],
        cutoff_time: datetime,
        filter_strategy: SatellitesFilterStrategy,
        runtime_settings: RuntimeSettings = RuntimeSettings(),
    ):
        self._cutoff_time = cutoff_time
        self._facility = facility
        self._antenna_positions = antenna_positions
        self._filter_strategy = filter_strategy(facility=facility, runtime_settings=runtime_settings)

    def run(self) -> List[List[PositionTime]]:
        segments_of_satellite_positions = []
        satellite_positions_in_view = []

        for antenna_position in self._antenna_positions_by_time:
            for satellite_position in self._sort_satellite_positions_by_time(satellite_positions=antenna_position.satellite_positions):

                if satellite_position.time >= self._cutoff_time:
                    break

                in_view = self._filter_strategy.is_in_view(satellite_position.position, antenna_position.antenna_direction.position)

                if in_view:
                    satellite_positions_in_view.append(satellite_position)
                elif satellite_positions_in_view:
                    segments_of_satellite_positions.append(satellite_positions_in_view)
                    satellite_positions_in_view = []

        if satellite_positions_in_view:
            segments_of_satellite_positions.append(satellite_positions_in_view)

        return segments_of_satellite_positions
    
    def power_run(self, satellite: Satellite) -> List[List[PowerTime]]:
        segments_of_power_times = []
        power_times_in_view = []

        for antenna_position in self._antenna_positions:
            for satellite_position in self._sort_satellite_positions_by_time(satellite_positions=antenna_position.satellite_positions):

                if satellite_position.time >= self._cutoff_time:
                    break

                in_view = self._filter_strategy.is_in_view(satellite_position.position, antenna_position.antenna_direction.position)

                if in_view:
                    power_times_in_view.append(self.convert_position_to_power(satellite, satellite_position))
                elif power_times_in_view:
                    segments_of_power_times.append(power_times_in_view)
                    power_times_in_view = []

        if power_times_in_view:
            segments_of_power_times.append(power_times_in_view)

        return segments_of_power_times
    
    def convert_position_to_power(self, satellite: Satellite, position_time: PositionTime) -> PowerTime:
        rec_gain = Facility.antenna.gain_pattern.get_gain
        trans_gain = satellite.antenna.gain_pattern.get_gain
        trans_pow = satellite.transmitter.power
        distance = position_time.position.distance_km
        wavelength = 10
        freespace_loss = ((4 * math.pi * distance)/wavelength)**2
        power_value = (trans_pow * trans_gain * rec_gain)/(freespace_loss)
        return PowerTime(power=power_value, time=position_time.time)
        

    @cached_property
    def _antenna_positions_by_time(self) -> List[AntennaPosition]:
        return sorted(self._antenna_positions, key=lambda x: x.antenna_direction.time)

    @staticmethod
    def _sort_satellite_positions_by_time(satellite_positions: List[PositionTime]) -> List[PositionTime]:
        return sorted(satellite_positions, key=lambda x: x.time)


class SatellitesAboveHorizonFilter(SatellitesFilterStrategy):
    def is_in_view(self, satellite_position: Position, antenna_position: Position) -> bool:
        return satellite_position.altitude >= self._runtime_settings.min_altitude


class SatellitesWithinMainBeamFilter(SatellitesFilterStrategy):
    def is_in_view(self, satellite_position: Position, antenna_position: Position) -> bool:
        return (
            self._is_within_beam_width_altitude(satellite_position.altitude, antenna_position.altitude)
            and self._is_within_beam_with_azimuth(satellite_position.azimuth, antenna_position.azimuth)
        )

    def _is_within_beam_width_altitude(self, satellite_altitude: float, antenna_altitude: float) -> bool:
        is_above_horizon = satellite_altitude >= self._runtime_settings.min_altitude
        lowest_main_beam_altitude = antenna_altitude - self._facility.half_beamwidth
        is_above_main_beam_altitude = satellite_altitude >= lowest_main_beam_altitude
        return is_above_horizon and is_above_main_beam_altitude

    def _is_within_beam_with_azimuth(self, satellite_azimuth: float, antenna_azimuth: float) -> bool:
        positions_to_compare_original = [satellite_azimuth, antenna_azimuth]
        positions_to_compare_next_modulus = (numpy.array(positions_to_compare_original) + DEGREES_IN_A_CIRCLE).tolist()
        positions_to_compare = itertools.combinations(positions_to_compare_original + positions_to_compare_next_modulus, 2)
        return any([isclose(*positions, abs_tol=self._facility.half_beamwidth) for positions in positions_to_compare])
