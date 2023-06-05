from dataclasses import replace
from datetime import timedelta
from functools import cached_property
from typing import List

from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder_rhodesmill.overhead_window_slew import AntennaPosition, \
    OverheadWindowSlew
from tests.event_finder.event_finder_rhodesmill.definitions import ARBITRARY_ANTENNA_POSITION, ARBITRARY_FACILITY


class TestOverheadWindowSlewOneAntennaPositionMultipleSatellitePositions:
    def test_one_satellite_with_a_few_overhead_windows(self):
        self._run_multiple_positions(satellite_positions=self._satellite_positions_by_time_ascending)

    def test_unsorted_satellite_positions(self):
        self._run_multiple_positions(satellite_positions=list(reversed(self._satellite_positions_by_time_ascending)))

    def _run_multiple_positions(self, satellite_positions: List[PositionTime]):
        cutoff_time = ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=len(self._satellite_positions_by_time_ascending))
        slew = OverheadWindowSlew(facility=ARBITRARY_FACILITY,
                                  antenna_positions=[AntennaPosition(satellite_positions=satellite_positions,
                                                                     antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                  cutoff_time=cutoff_time)
        windows = slew.run()
        assert windows == [
            TimeWindow(begin=self._satellite_positions_by_time_ascending[i].time,
                       end=self._satellite_positions_by_time_ascending[i + 1].time
                       if i + 1 < len(self._satellite_positions_by_time_ascending)
                       else cutoff_time)
            for i in range(0, len(self._satellite_positions_by_time_ascending), 2)
        ]

    @cached_property
    def _satellite_positions_by_time_ascending(self) -> List[PositionTime]:
        small_epsilon = 1e-3
        value_slightly_larger_than_half_beamwidth = ARBITRARY_FACILITY.beamwidth - small_epsilon
        out_of_altitude = ARBITRARY_ANTENNA_POSITION.altitude + value_slightly_larger_than_half_beamwidth
        return [
            replace(ARBITRARY_ANTENNA_POSITION,
                    altitude=out_of_altitude if i % 2 else ARBITRARY_ANTENNA_POSITION.altitude,
                    time=ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=i))
            for i in range(5)
        ]
