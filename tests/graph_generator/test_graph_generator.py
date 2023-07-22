from datetime import datetime
from typing import List

from numpy import asarray
from numpy.ma import allequal

from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.graph_generator import graph_generator
from satellite_determination.graph_generator.graph_generator import GraphGenerator

class TestGraphGenerator:

    def test_generate_graph(self, mocker):
        mock = mocker.patch.object(graph_generator, 'plt')
        GraphGenerator(search_window_start=self._arbitrary_search_window_start,
                       search_window_end=self._arbitrary_search_window_end,
                       satellites_above_horizon=self._arbitrary_overhead_window,
                       interference_windows=self._arbitrary_overhead_window_two).generate_graph()
        assert allequal(mock.bar.call_args_list[0].args[0], asarray([0, 1, 2, 3, 4, 5, 6, 7, 8]) - 0.2)
        assert allequal(mock.bar.call_args_list[0].args[1], [0, 0, 1, 0, 0, 0, 0, 0, 0])
        assert mock.bar.call_args_list[0].args[2] == 0.4
        assert mock.bar.call_args_list[0].kwargs == {'label': 'Satellites above the horizon'}

        assert allequal(mock.bar.call_args_list[1].args[0], asarray([0, 1, 2, 3, 4, 5, 6, 7, 8]) + 0.2)
        assert allequal(mock.bar.call_args_list[1].args[1], [0, 0, 1, 0, 0, 0, 0, 0, 0])
        assert mock.bar.call_args_list[1].args[2] == 0.4
        assert mock.bar.call_args_list[1].kwargs == {'label': 'Satellites crossing main observation beam'}

        mock.xlabel.assert_called_with('Hour (UTC)')
        mock.ylabel.assert_called_with('Number of satellites')
        mock.title.assert_called_with('Overhead Satellites at HCRO starting at 2023-04-18 23:00:00')
        mock.legend.assert_called()

        assert allequal(mock.xticks.call_args.args[0], [0, 1, 2, 3, 4, 5, 6, 7, 8])
        assert allequal(mock.xticks.call_args.args[1], ['23', '0', '1', '2', '3', '4', '5', '6', '7'])

        mock.show.assert_called()

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

