from datetime import datetime

import pytz

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.position import Position
from satellite_determination.custom_dataclasses.position_time import PositionTime

ARBITRARY_FACILITY = Facility(coordinates=Coordinates(latitude=0, longitude=0))

ARBITRARY_ANTENNA_POSITION = PositionTime(position=Position(altitude=100, azimuth=100), time=datetime.now(tz=pytz.UTC))
