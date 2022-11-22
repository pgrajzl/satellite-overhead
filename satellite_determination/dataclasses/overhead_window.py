from dataclasses import dataclass

from satellite_determination.dataclasses.satellite import Satellite
from satellite_determination.dataclasses.time_window import TimeWindow


@dataclass
class OverheadWindow:
    satellite: Satellite
    overhead_time: TimeWindow
