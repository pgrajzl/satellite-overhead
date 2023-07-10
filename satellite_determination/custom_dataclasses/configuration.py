from dataclasses import dataclass
from typing import Optional

from satellite_determination.custom_dataclasses.observation_target import ObservationTarget
from satellite_determination.custom_dataclasses.position import Position
from satellite_determination.custom_dataclasses.reservation import Reservation


@dataclass
class Configuration:
    reservation: Reservation
    observation_target: Optional[ObservationTarget] = None
    static_antenna_position:  Optional[Position] = None
