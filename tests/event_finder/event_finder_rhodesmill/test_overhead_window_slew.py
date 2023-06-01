from dataclasses import replace
from datetime import datetime, timedelta
from functools import cached_property

import pytz

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder_rhodesmill.overhead_window_slew import OverheadWindowSlew, \
    AntennaPosition


class TestOverheadWindowSlew:
    def test_no_satellite_positions(self):
        slew = OverheadWindowSlew(facility=self._arbitrary_facility,
                                  antenna_positions=[AntennaPosition(satellite_positions=[],
                                                                     antenna_direction=self._arbitrary_antenna_position)],
                                  cutoff_time=self._arbitrary_cutoff_time)
        windows = slew.run()
        assert windows == []

    def test_one_satellite_position_exactly_at_antenna_position(self):
        satellite_positions = [
            self._arbitrary_antenna_position
        ]
        cutoff_time = self._arbitrary_antenna_position.time + timedelta(minutes=1)
        slew = OverheadWindowSlew(facility=self._arbitrary_facility,
                                  antenna_positions=[AntennaPosition(satellite_positions=satellite_positions,
                                                                     antenna_direction=self._arbitrary_antenna_position)],
                                  cutoff_time=cutoff_time)
        windows = slew.run()
        assert windows == [TimeWindow(begin=self._arbitrary_antenna_position.time, end=cutoff_time)]

    def test_one_satellite_position_outside_beamwidth_altitude(self):
        satellite_positions = [
            replace(self._arbitrary_antenna_position,
                    altitude=self._arbitrary_antenna_position.altitude - self._value_slightly_larger_than_half_beamwidth)
        ]
        slew = OverheadWindowSlew(facility=self._arbitrary_facility,
                                  antenna_positions=[AntennaPosition(satellite_positions=satellite_positions,
                                                                     antenna_direction=self._arbitrary_antenna_position)],
                                  cutoff_time=self._arbitrary_cutoff_time)
        windows = slew.run()
        assert windows == []

    def test_one_satellite_position_outside_beamwidth_azimuth(self):
        satellite_positions = [
            replace(self._arbitrary_antenna_position,
                    azimuth=self._arbitrary_antenna_position.azimuth - self._value_slightly_larger_than_half_beamwidth)
        ]
        slew = OverheadWindowSlew(facility=self._arbitrary_facility,
                                  antenna_positions=[AntennaPosition(satellite_positions=satellite_positions,
                                                                     antenna_direction=self._arbitrary_antenna_position)],
                                  cutoff_time=self._arbitrary_cutoff_time)
        windows = slew.run()
        assert windows == []

    def test_one_satellite_with_a_few_overhead_windows(self):
        out_of_altitude = self._arbitrary_antenna_position.altitude + self._value_slightly_larger_than_half_beamwidth
        satellite_positions = [
            replace(self._arbitrary_antenna_position,
                    altitude=out_of_altitude if i % 2 else self._arbitrary_antenna_position.altitude,
                    time=self._arbitrary_antenna_position.time + timedelta(minutes=i))
            for i in range(5)
        ]
        cutoff_time = self._arbitrary_antenna_position.time + timedelta(minutes=len(satellite_positions))
        slew = OverheadWindowSlew(facility=self._arbitrary_facility,
                                  antenna_positions=[AntennaPosition(satellite_positions=satellite_positions,
                                                                     antenna_direction=self._arbitrary_antenna_position)],
                                  cutoff_time=cutoff_time)
        windows = slew.run()
        assert windows == [
            TimeWindow(begin=satellite_positions[i].time,
                       end=satellite_positions[i + 1].time
                           if i + 1 < len(satellite_positions)
                           else cutoff_time)
            for i in range(0, len(satellite_positions), 2)
        ]

    def test_one_satellite_with_multiple_sequential_positions_in_view(self):
        out_of_altitude = self._arbitrary_antenna_position.altitude + self._value_slightly_larger_than_half_beamwidth
        satellite_positions = [
            replace(self._arbitrary_antenna_position,
                    altitude=out_of_altitude if i == 2 else self._arbitrary_antenna_position.altitude,
                    time=self._arbitrary_antenna_position.time + timedelta(minutes=i))
            for i in range(3)
        ]
        cutoff_time = self._arbitrary_antenna_position.time + timedelta(minutes=len(satellite_positions))
        slew = OverheadWindowSlew(facility=self._arbitrary_facility,
                                  antenna_positions=[
                                      AntennaPosition(satellite_positions=satellite_positions,
                                                      antenna_direction=self._arbitrary_antenna_position)],
                                  cutoff_time=cutoff_time)
        windows = slew.run()
        assert windows == [
            TimeWindow(begin=satellite_positions[0].time, end=satellite_positions[-1].time)
        ]

    def test_one_satellite_with_multiple_sequential_positions_out_of_view(self):
        out_of_altitude = self._arbitrary_antenna_position.altitude + self._value_slightly_larger_than_half_beamwidth
        satellite_positions = [
            replace(self._arbitrary_antenna_position,
                    altitude=out_of_altitude if 0 < i < 3 else self._arbitrary_antenna_position.altitude,
                    time=self._arbitrary_antenna_position.time + timedelta(minutes=i))
            for i in range(4)
        ]
        cutoff_time = self._arbitrary_antenna_position.time + timedelta(minutes=len(satellite_positions))
        slew = OverheadWindowSlew(facility=self._arbitrary_facility,
                                  antenna_positions=[
                                      AntennaPosition(satellite_positions=satellite_positions,
                                                      antenna_direction=self._arbitrary_antenna_position)],
                                  cutoff_time=cutoff_time)
        windows = slew.run()
        assert windows == [
            TimeWindow(begin=satellite_positions[0].time, end=satellite_positions[1].time),
            TimeWindow(begin=satellite_positions[3].time, end=cutoff_time),
        ]

    def test_multiple_antenna_positions(self):
        arbitrary_antenna_position2 = PositionTime(altitude=200, azimuth=200, time=self._arbitrary_antenna_position.time + timedelta(minutes=1))
        cutoff_time = arbitrary_antenna_position2.time + timedelta(minutes=1)
        slew = OverheadWindowSlew(facility=self._arbitrary_facility,
                                  antenna_positions=[
                                      AntennaPosition(satellite_positions=[self._arbitrary_antenna_position],
                                                      antenna_direction=self._arbitrary_antenna_position),
                                      AntennaPosition(satellite_positions=[arbitrary_antenna_position2],
                                                      antenna_direction=arbitrary_antenna_position2)
                                  ],
                                  cutoff_time=cutoff_time)
        windows = slew.run()
        assert windows == [
            TimeWindow(begin=self._arbitrary_antenna_position.time, end=cutoff_time)
        ]

    def test_one_satellite_below_horizon_but_within_beamwidth(self):
        antenna_position_at_horizon = replace(self._arbitrary_antenna_position, altitude=0)
        satellite_positions = [
            replace(antenna_position_at_horizon, altitude=-self._small_epsilon)
        ]
        slew = OverheadWindowSlew(facility=self._arbitrary_facility,
                                  antenna_positions=[
                                      AntennaPosition(satellite_positions=satellite_positions,
                                                      antenna_direction=antenna_position_at_horizon)],
                                  cutoff_time=self._arbitrary_cutoff_time)
        windows = slew.run()
        assert windows == []

    @property
    def _value_slightly_larger_than_half_beamwidth(self) -> float:
        return self._arbitrary_facility.beamwidth - self._small_epsilon

    @property
    def _small_epsilon(self) -> float:
        return 1e-3

    @property
    def _arbitrary_cutoff_time(self) -> datetime:
        return datetime.now()

    @property
    def _arbitrary_facility(self) -> Facility:
        return Facility(point_coordinates=Coordinates(latitude=0, longitude=0))

    @cached_property
    def _arbitrary_antenna_position(self) -> PositionTime:
        return PositionTime(altitude=100, azimuth=100, time=datetime.now(tz=pytz.UTC))
