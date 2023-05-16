from dataclasses import dataclass
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.time_window import TimeWindow

'''
OverheadWindow class is designed to store the time windows that a given satellite is overhead and includes the Satellite object,
as well as a TimeWindow object that contains the interference start and end times.

  + satellite:      the Satellite that is overhead during the time window.
  + overhead_time:  a TimeWindow representing the time the satellite enters and exits view.
'''

@dataclass
class OverheadWindow:
    satellite: Satellite
    overhead_time: TimeWindow
