from datetime import datetime, timedelta
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.time_window import TimeWindow


class GraphGenerator:

    def __init__(self, search_window_start: datetime, search_window_end: datetime, satellites_above_horizon: List[OverheadWindow], interference_windows: List[OverheadWindow]):
        self._satellite_above_horizon = satellites_above_horizon
        self._interference_windows = interference_windows
        self._search_window_start = search_window_start
        self._search_window_end = search_window_end

    def generate_graph(self):
        search_intervals = []
        num_sats_above_horizon = []
        num_sats_beam = []
        start_interval = self._search_window_start
        while start_interval < self._search_window_end:
            search_intervals.append(start_interval)
            start_interval+=timedelta(hours=1)
        x_axis = []
        for interval in search_intervals:
            x_axis.append(str(interval.hour))
            interval_window = TimeWindow(
                begin=interval,
                end=interval+timedelta(minutes=59)
            )
            sats_horizon = []
            sats_beam = []
            for window in self._satellite_above_horizon:
                if window.overhead_time.overlaps(interval_window):
                    sats_horizon.append(window)
            for window in self._interference_windows:
                if window.overhead_time.overlaps(interval_window):
                    sats_beam.append(window)
            num_sats_above_horizon.append(len(sats_horizon))
            num_sats_beam.append(len(sats_beam))
        size_x_axis = np.arange(len(x_axis))
        plt.bar(size_x_axis - 0.2, num_sats_above_horizon, 0.4, label='Sats above horizon')
        plt.bar(size_x_axis + 0.2, num_sats_beam, 0.4, label='Sats in beam')
        plt.xticks(size_x_axis, x_axis)
        plt.show()

