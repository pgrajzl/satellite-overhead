from dataclasses import dataclass
from skyfield.api import EarthSatellite
from satellite_determination.dataclasses.skyfield_satellite import SkyfieldSatelliteList
from satellite_determination.dataclasses.time_window import TimeWindow


@dataclass
class OverheadWindow:
    satellite_name: EarthSatellite
    overhead_time: TimeWindow
