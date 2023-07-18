from datetime import datetime
from typing import List

from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.graph_generator.graph_generator import GraphGenerator

class TestGraphGenerator:

    def test_generate_graph(self):
        graphs = GraphGenerator(search_window_start=self._arbitrary_search_window_start,
                                search_window_end=self._arbitrary_search_window_end,
                                satellites_above_horizon=self._arbitrary_overhead_window,
                                interference_windows=self._arbitrary_overhead_window_two).generate_graph()
        return graphs

    @property
    def _arbitrary_overhead_window(self) -> List[OverheadWindow]:
        return [OverheadWindow(
                satellite=None,
                overhead_time=TimeWindow(
                    begin=datetime(year=2023, month=4, day=19, hour=1),
                    end=datetime(year=2023, month=4, day=19, hour=2)
                )
            )]

    @property
    def _arbitrary_overhead_window_two(self) -> List[OverheadWindow]:
        return [OverheadWindow(
            satellite=None,
            overhead_time=TimeWindow(
                begin=datetime(year=2023, month=4, day=19, hour=1),
                end=datetime(year=2023, month=4, day=19, hour=2)
            )
        )]

    @property
    def _arbitrary_search_window_start(self) -> datetime:
        return datetime(year=2023, month=4, day=18, hour=23)

    @property
    def _arbitrary_search_window_end(self) -> datetime:
        return datetime(year=2023, month=4, day=19, hour=7)

