import pytest
import pytz
from datetime import datetime

from sopp.sopp import Sopp
from sopp.custom_dataclasses.overhead_window import OverheadWindow
from sopp.custom_dataclasses.configuration import Configuration
from sopp.custom_dataclasses.satellite.satellite import Satellite
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.custom_dataclasses.position import Position


class TestSopp:
    def test_get_satellites_above_horizon(self):
        assert overhead_windows() == self._sopp.get_satellites_above_horizon()

    def test_get_satellites_crossing_main_beam(self):
        assert overhead_windows() == self._sopp.get_satellites_crossing_main_beam()

    @property
    def _sopp(self):
        sopp = Sopp(configuration=self._configuration, event_finder_class=StubEventFinder)
        return sopp

    @property
    def _configuration(self):
        configuration = Configuration(
            satellites='holder',
            antenna_direction_path='holder',
            reservation='holder',
        )
        return configuration


class StubEventFinder:
    def __init__(self, list_of_satellites, reservation, antenna_direction_path, runtime_settings):
        pass

    def get_satellites_above_horizon(self):
        return overhead_windows()

    def get_satellites_crossing_main_beam(self):
        return overhead_windows()

def overhead_windows():
    return [
        OverheadWindow(
            satellite=Satellite(name='TestSatellite'),
            positions=[
                PositionTime(
                    position=Position(altitude=31.92827689000652, azimuth=322.2152123600712),
                    time=datetime(2023, 3, 30, 14, 39, 32, tzinfo=pytz.UTC)
                ),
                PositionTime(
                    position=Position(altitude=32.10476096624609, azimuth=321.73184343501606),
                    time=datetime(2023, 3, 30, 14, 39, 33, tzinfo=pytz.UTC)
                ),
                PositionTime(
                    position=Position(altitude=32.28029629612362, azimuth=321.24277001092725),
                    time=datetime(2023, 3, 30, 14, 39, 34, tzinfo=pytz.UTC)
                ),
                PositionTime(
                    position=Position(altitude=32.45481011166138, azimuth=320.74796378603236),
                    time=datetime(2023, 3, 30, 14, 39, 35, tzinfo=pytz.UTC)
                )
            ]
        ),
        OverheadWindow(
            satellite=Satellite(name='TestSatellite2'),
            positions=[
                PositionTime(
                    position=Position(altitude=0.011527751634842421, azimuth=31.169677715036304),
                    time=datetime(2023, 3, 30, 14, 39, 35, tzinfo=pytz.UTC)
                )
            ]
        )
    ]
