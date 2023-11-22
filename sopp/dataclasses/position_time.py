from dataclasses import dataclass
from datetime import datetime

from sopp.dataclasses.position import Position


@dataclass
class PositionTime:
    position: Position
    time: datetime
