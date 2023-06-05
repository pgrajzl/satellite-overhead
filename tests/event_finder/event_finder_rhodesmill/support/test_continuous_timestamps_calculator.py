from datetime import datetime, timedelta

from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder_rhodesmill.support.pseudo_continuous_timestamps_calculator import \
    PseudoContinuousTimestampsCalculator


class TestPseudoContinuousTimestampsCalculator:
    def test_resolution_divides_timewindow_exactly(self):
        arbitrary_start_time = datetime(year=2023, month=6, day=5)
        arbitrary_time_window = TimeWindow(
            begin=arbitrary_start_time,
            end=arbitrary_start_time + timedelta(seconds=3)
        )
        timestamps = PseudoContinuousTimestampsCalculator(time_window=arbitrary_time_window).run()
        assert timestamps == [
            datetime(year=2023, month=6, day=5),
            datetime(year=2023, month=6, day=5, second=1),
            datetime(year=2023, month=6, day=5, second=2)
        ]

    def test_resolution_does_not_divide_timewindow_exactly(self):
        arbitrary_start_time = datetime(year=2023, month=6, day=5)
        arbitrary_time_window = TimeWindow(
            begin=arbitrary_start_time,
            end=arbitrary_start_time + timedelta(seconds=3)
        )
        timestamps = PseudoContinuousTimestampsCalculator(time_window=arbitrary_time_window, resolution=timedelta(seconds=1.7)).run()
        assert timestamps == [
            datetime(year=2023, month=6, day=5),
            datetime(year=2023, month=6, day=5, second=1, microsecond=int(7e5))
        ]
