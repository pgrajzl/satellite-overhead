from dataclasses import dataclass

import pytz

from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.time_window import TimeWindow


@dataclass
class OverheadWindow:
    satellite: Satellite
    overhead_time: TimeWindow

    def __int__(self, satellite: Satellite, overhead_time: TimeWindow):
        super().__init__(satellite, overhead_time)
        assert overhead_time.timezone == pytz.UTC
