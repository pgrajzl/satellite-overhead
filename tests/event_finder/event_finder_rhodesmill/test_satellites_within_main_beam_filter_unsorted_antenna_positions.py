from datetime import timedelta
from typing import List

from sopp.custom_dataclasses.position import Position
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.event_finder.event_finder_rhodesmill.support.satellites_within_main_beam_filter import AntennaPosition, \
    SatellitesWithinMainBeamFilter
from tests.event_finder.event_finder_rhodesmill.definitions import ARBITRARY_ANTENNA_POSITION, ARBITRARY_FACILITY, create_expected_windows, assert_windows_eq


class TestSatellitesWithinMainBeamMultipleAntennas:
    def test_multiple_antenna_positions(self):
        self._run_multiple_positions(antenna_positions=self._antenna_positions_sorted_by_time_ascending)

    def test_unsorted_antenna_positions(self):
        self._run_multiple_positions(antenna_positions=list(reversed(self._antenna_positions_sorted_by_time_ascending)))

    def _run_multiple_positions(self, antenna_positions: List[PositionTime]):
        cutoff_time = self._antenna_positions_sorted_by_time_ascending[-1].time + timedelta(minutes=1)
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[
                                                  AntennaPosition(satellite_positions=[antenna_position],
                                                                  antenna_direction=antenna_position)
                                                  for antenna_position in antenna_positions
                                              ],
                                              cutoff_time=cutoff_time)
        windows = slew.run()
        expected_positions = [self._antenna_positions_sorted_by_time_ascending[::]]
        expected_windows = create_expected_windows(expected_positions)

        assert len(windows) == 1
        assert_windows_eq(windows, expected_windows)

    @property
    def _antenna_positions_sorted_by_time_ascending(self) -> List[PositionTime]:
        arbitrary_antenna_position2 = PositionTime(position=Position(altitude=200, azimuth=200),
                                                   time=ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=1))
        return [ARBITRARY_ANTENNA_POSITION, arbitrary_antenna_position2]
