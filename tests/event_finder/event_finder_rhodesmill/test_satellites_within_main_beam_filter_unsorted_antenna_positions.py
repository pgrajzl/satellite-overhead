from datetime import timedelta
from typing import List

from satellite_determination.custom_dataclasses.position import Position
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellites_within_main_beam_filter import AntennaPosition, \
    SatellitesWithinMainBeamFilter
from tests.event_finder.event_finder_rhodesmill.definitions import ARBITRARY_ANTENNA_POSITION, ARBITRARY_FACILITY


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
        assert windows[0][0] == ARBITRARY_ANTENNA_POSITION
        assert windows[0][-1].time == cutoff_time - timedelta(minutes=1)

    @property
    def _antenna_positions_sorted_by_time_ascending(self) -> List[PositionTime]:
        arbitrary_antenna_position2 = PositionTime(position=Position(altitude=200, azimuth=200),
                                                   time=ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=1))
        return [ARBITRARY_ANTENNA_POSITION, arbitrary_antenna_position2]
