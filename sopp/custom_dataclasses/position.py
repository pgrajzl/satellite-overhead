from dataclasses import dataclass


@dataclass
class Position:
    """
    + altitude: degrees above the horizon
    + azimuth: degrees east along the horizon from geographic north (so 0 degrees means north, 90 is east, 180
        is south, and 270 is west).
    """
    altitude: float
    azimuth: float
