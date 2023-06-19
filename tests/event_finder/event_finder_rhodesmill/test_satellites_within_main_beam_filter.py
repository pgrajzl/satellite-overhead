from dataclasses import replace
from datetime import datetime, timedelta

from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellites_within_main_beam_filter import SatellitesWithinMainBeamFilter, \
    AntennaPosition
from tests.event_finder.event_finder_rhodesmill.definitions import ARBITRARY_ANTENNA_POSITION, ARBITRARY_FACILITY


class TestSatellitesWithinMainBeam:
    def test_no_satellite_positions(self):
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[AntennaPosition(satellite_positions=[],
                                                                                 antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=self._arbitrary_cutoff_time)
        windows = slew.run()
        assert windows == []

    def test_one_satellite_position_exactly_at_antenna_position(self):
        satellite_positions = [
            ARBITRARY_ANTENNA_POSITION
        ]
        cutoff_time = ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=1)
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[AntennaPosition(satellite_positions=satellite_positions,
                                                                                 antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=cutoff_time)
        windows = slew.run()
        assert windows == [TimeWindow(begin=ARBITRARY_ANTENNA_POSITION.time, end=cutoff_time)]

    def test_one_satellite_position_outside_beamwidth_altitude(self):
        satellite_positions = [
            replace(ARBITRARY_ANTENNA_POSITION,
                    altitude=ARBITRARY_ANTENNA_POSITION.altitude - self._value_slightly_larger_than_half_beamwidth)
        ]
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[AntennaPosition(satellite_positions=satellite_positions,
                                                                                 antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=self._arbitrary_cutoff_time)
        windows = slew.run()
        assert windows == []

    def test_one_satellite_position_outside_beamwidth_azimuth(self):
        satellite_positions = [
            replace(ARBITRARY_ANTENNA_POSITION,
                    azimuth=ARBITRARY_ANTENNA_POSITION.azimuth - self._value_slightly_larger_than_half_beamwidth)
        ]
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[AntennaPosition(satellite_positions=satellite_positions,
                                                                                 antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=self._arbitrary_cutoff_time)
        windows = slew.run()
        assert windows == []

    def test_one_satellite_with_multiple_sequential_positions_in_view(self):
        out_of_altitude = ARBITRARY_ANTENNA_POSITION.altitude + self._value_slightly_larger_than_half_beamwidth
        satellite_positions = [
            replace(ARBITRARY_ANTENNA_POSITION,
                    altitude=out_of_altitude if i == 2 else ARBITRARY_ANTENNA_POSITION.altitude,
                    time=ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=i))
            for i in range(3)
        ]
        cutoff_time = ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=len(satellite_positions))
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[
                                                  AntennaPosition(satellite_positions=satellite_positions,
                                                                  antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=cutoff_time)
        windows = slew.run()
        assert windows == [
            TimeWindow(begin=satellite_positions[0].time, end=satellite_positions[-1].time)
        ]

    def test_one_satellite_with_multiple_sequential_positions_out_of_view(self):
        out_of_altitude = ARBITRARY_ANTENNA_POSITION.altitude + self._value_slightly_larger_than_half_beamwidth
        satellite_positions = [
            replace(ARBITRARY_ANTENNA_POSITION,
                    altitude=out_of_altitude if 0 < i < 3 else ARBITRARY_ANTENNA_POSITION.altitude,
                    time=ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=i))
            for i in range(4)
        ]
        cutoff_time = ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=len(satellite_positions))
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[
                                                  AntennaPosition(satellite_positions=satellite_positions,
                                                                  antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=cutoff_time)
        windows = slew.run()
        assert windows == [
            TimeWindow(begin=satellite_positions[0].time, end=satellite_positions[1].time),
            TimeWindow(begin=satellite_positions[3].time, end=cutoff_time),
        ]

    @property
    def _value_slightly_larger_than_half_beamwidth(self) -> float:
        return ARBITRARY_FACILITY.beamwidth - self._small_epsilon

    def test_one_satellite_below_horizon_but_within_beamwidth(self):
        antenna_position_at_horizon = replace(ARBITRARY_ANTENNA_POSITION, altitude=0)
        satellite_positions = [
            replace(antenna_position_at_horizon, altitude=-self._small_epsilon)
        ]
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[
                                                  AntennaPosition(satellite_positions=satellite_positions,
                                                                  antenna_direction=antenna_position_at_horizon)],
                                              cutoff_time=self._arbitrary_cutoff_time)
        windows = slew.run()
        assert windows == []

    @property
    def _small_epsilon(self) -> float:
        return 1e-3

    @property
    def _arbitrary_cutoff_time(self) -> datetime:
        return datetime.now()
