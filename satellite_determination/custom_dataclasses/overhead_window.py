from dataclasses import dataclass
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.time_window import TimeWindow


@dataclass
class OverheadWindow:
    satellite: Satellite
    overhead_time: TimeWindow
