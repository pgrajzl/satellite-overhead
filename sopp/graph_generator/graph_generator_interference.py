import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta
import numpy as np


class GraphGeneratorInterference:
    def __init__(self, start_time, end_time, interference_data, title):
        self._start_time = start_time
        self._end_time = end_time
        self._title = title

        self._interference_data = sorted(interference_data, key=lambda x: x.time)

        self._x_axis = self._create_x_axis()
        self._interference_counts = self._calculate_interference_counts()

    def _create_x_axis(self):
        x_axis = mdates.drange(self._start_time, self._end_time, timedelta(seconds=1))
        return [mdates.num2date(x) for x in x_axis]

    def _calculate_interference_counts(self):
        interference_counts = [0] * len(self._x_axis)
        for pt in self._interference_data:
            index = self._x_axis.index(pt.time)
            interference_counts[index] += 1
        return interference_counts

    def _normalize_counts(self, counts):
        min_count = min(counts)
        max_count = max(counts)
        return np.array([(c - min_count) / (max_count - min_count) for c in counts])

    def generate_graph(self):
        fig, ax = plt.subplots(figsize=(25, 10))

        normalized_counts = self._normalize_counts(self._interference_counts)
        cmap = plt.get_cmap('Blues')

        #ax.plot(self._x_axis, self._interference_counts, color=cmap(normalized_counts), label='Interference', linewidth=2)
        #ax.fill_between(self._x_axis, self._interference_counts, color=cmap(normalized_counts), alpha=0.3)

        ax.plot(self._x_axis, self._interference_counts, color='red', label='Interference')
        ax.fill_between(self._x_axis, self._interference_counts, color='red', alpha=0.3)

        #ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        ax.set_xlabel('Time UTC')
        ax.set_ylabel('Satellites Crossing Main Beam Count')
        ax.set_title(self._title)
        ax.grid(axis='y')
        ax.legend()

        plt.show()

