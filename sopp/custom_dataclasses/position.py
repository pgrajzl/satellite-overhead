from dataclasses import dataclass
from typing import Optional

import math
from sopp.event_finder.event_finder_rhodesmill.support.satellite_link_budget_angle_calc import CartesianCoordinate


@dataclass
class Position:
    """
    Represents a position relative to an observer on Earth.

    Attributes:
    + altitude (float): The altitude angle of the object in degrees. It ranges
      from 0° at the horizon to 90° directly overhead at the zenith. A negative
      altitude means the satellite is below the horizon.
    + azimuth (float): The azimuth angle of the object in degrees, measured
      clockwise around the horizon. It runs from 0° (geographic north) through
      east (90°), south (180°), and west (270°) before returning to the north.
    + distance (Optional[float]): The straight-line distance between the
      object and the observer in kilometers. If not provided, it is set to
      None.
    """
    altitude: float
    azimuth: float
    distance_km: Optional[float] = None

    def to_cartesian(self) -> CartesianCoordinate:
        if self.distance_km is None:
            raise ValueError("Distance must be provided to convert to Cartesian coordinates.")
        
        # Convert angles to radians
        theta = math.radians(90 - self.altitude)
        phi = math.radians(self.azimuth)
        
        # Convert to Cartesian coordinates
        x = self.distance_km * math.sin(theta) * math.cos(phi)
        y = self.distance_km * math.sin(theta) * math.sin(phi)
        z = self.distance_km * math.cos(theta)
        
        return CartesianCoordinate(x, y, z)