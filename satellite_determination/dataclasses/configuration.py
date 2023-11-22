from dataclasses import dataclass
from typing import List, Optional

from satellite_determination.dataclasses.observation_target import ObservationTarget
from satellite_determination.dataclasses.position import Position
from satellite_determination.dataclasses.position_time import PositionTime
from satellite_determination.dataclasses.reservation import Reservation
from satellite_determination.dataclasses.runtime_settings import RuntimeSettings


@dataclass
class Configuration:
    reservation: Reservation
    runtime_settings: Optional[RuntimeSettings] = RuntimeSettings()
    antenna_position_times: Optional[List[PositionTime]] = None
    observation_target: Optional[ObservationTarget] = None
    static_antenna_position: Optional[Position] = None
