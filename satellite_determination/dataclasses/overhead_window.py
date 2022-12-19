from dataclasses import dataclass
from skyfield.api import EarthSatellite
from satellite_determination.dataclasses.skyfield_satellite import SkyfieldSatellite
from satellite_determination.dataclasses.time_window import TimeWindow


@dataclass
class OverheadWindow:
    satellite: SkyfieldSatellite
    overhead_time: TimeWindow
