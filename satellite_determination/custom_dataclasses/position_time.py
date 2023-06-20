from dataclasses import dataclass
from datetime import datetime


@dataclass
class PositionTime:
    """
    + altitude: degrees above the horizon
    + azimuth: degrees east along the horizon from geographic north (so 0 degrees means north, 90 is east, 180
        is south, and 270 is west).
    + time: a timestamp
    """
    altitude: float
    azimuth: float
    time: datetime
