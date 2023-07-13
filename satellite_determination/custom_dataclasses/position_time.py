from dataclasses import dataclass
from datetime import datetime

from satellite_determination.custom_dataclasses.position import Position


@dataclass
class PositionTime:
    position: Position
    time: datetime
