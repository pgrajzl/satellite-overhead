from dataclasses import dataclass
from typing import List, Optional

from sopp.dataclasses.observation_target import ObservationTarget
from sopp.dataclasses.position import Position
from sopp.dataclasses.position_time import PositionTime
from sopp.dataclasses.reservation import Reservation
from sopp.dataclasses.runtime_settings import RuntimeSettings


@dataclass
class Configuration:
    reservation: Reservation
    runtime_settings: Optional[RuntimeSettings] = RuntimeSettings()
    antenna_position_times: Optional[List[PositionTime]] = None
    observation_target: Optional[ObservationTarget] = None
    static_antenna_position: Optional[Position] = None
