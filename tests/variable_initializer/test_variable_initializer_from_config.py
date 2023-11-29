from datetime import datetime

import pytest
import pytz

from sopp.variable_initializer.variable_initializer_from_config import VariableInitializerFromConfig
from sopp.satellites_loader.satellites_loader import SatellitesLoader
from sopp.custom_dataclasses.satellite.satellite import Satellite
from sopp.custom_dataclasses.configuration import Configuration
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.facility import Facility
from sopp.custom_dataclasses.coordinates import Coordinates
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.custom_dataclasses.observation_target import ObservationTarget
from sopp.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from sopp.custom_dataclasses.position import Position
from sopp.custom_dataclasses.position_time import PositionTime

class StubSatellitesLoader(SatellitesLoader):
    def load_satellites(self):
        return [
            Satellite(name='Satellite1'),
            Satellite(name='Satellite2'),
        ]

class TestVariableInitializerFromConfig:
    @property
    def common_config(self):
        return Configuration(
            reservation=Reservation(
                facility=Facility(
                    coordinates=Coordinates(latitude=40.8178049, longitude=-121.4695413),
                    beamwidth=3,
                    elevation=100,
                    name='ARBITRARY_2'
                ),
                time=TimeWindow(
                    begin=datetime(year=2023, month=3, day=30, hour=10, tzinfo=pytz.utc),
                    end=datetime(year=2023, month=3, day=30, hour=15, tzinfo=pytz.utc)
                ),
                frequency=FrequencyRange(frequency=135, bandwidth=10, status=None)
            ),
            antenna_position_times=None,
            observation_target=None,
            static_antenna_position=None,
        )

    @property
    def observation_config(self):
        config = self.common_config
        config.observation_target = ObservationTarget(
            declination='-38d6m50.8s',
            right_ascension='4h42m'
        )
        return config

    @property
    def static_config(self):
        config = self.common_config
        config.static_antenna_position = Position(altitude=.2, azimuth=.3)
        return config

    @property
    def antenna_position_config(self):
        config = self.common_config
        config.antenna_position_times = [
            PositionTime(
                position=Position(altitude=.0, azimuth=.1),
                time=datetime(year=2023, month=3, day=30, hour=10, minute=1, tzinfo=pytz.UTC)
            ),
            PositionTime(
                position=Position(altitude=.1, azimuth=.2),
                time=datetime(year=2023, month=3, day=30, hour=10, minute=2, tzinfo=pytz.UTC)
            )
        ]
        return config

    @property
    def stub_satellites_loader(self):
        return StubSatellitesLoader()

    def test_get_reservation(self):
        var_initializer = VariableInitializerFromConfig(
                satellites_loader=self.stub_satellites_loader,
                config=self.observation_config
        )
        
        reservation = var_initializer.get_reservation()
        assert reservation == Reservation(
            facility=Facility(
                coordinates=Coordinates(latitude=40.8178049, longitude=-121.4695413),
                beamwidth=3,
                elevation=100,
                name='ARBITRARY_2'
            ),
            time=TimeWindow(
                begin=datetime(year=2023, month=3, day=30, hour=10, tzinfo=pytz.utc),
                end=datetime(year=2023, month=3, day=30, hour=15, tzinfo=pytz.utc)
            ),
            frequency=FrequencyRange(frequency=135, bandwidth=10, status=None)
        )

    def test_get_satellite_list(self):
        var_initializer = VariableInitializerFromConfig(
            satellites_loader=self.stub_satellites_loader,
            config=self.common_config
        )

        satellite_list = var_initializer.get_satellite_list()
        assert satellite_list == [
            Satellite(name='Satellite1'),
            Satellite(name='Satellite2'),
        ]

    def test_get_antenna_direction_path_observation_config(self):
        var_initializer = VariableInitializerFromConfig(
                satellites_loader=self.stub_satellites_loader,
                config=self.observation_config
        )

        antenna_direction_path = var_initializer.get_antenna_direction_path()
        assert antenna_direction_path[0] == PositionTime(
            position=Position(altitude=-63.291283818128676, azimuth=264.47226741909765),
            time=datetime(year=2023, month=3, day=30, hour=10, minute=0, tzinfo=pytz.UTC)
        )
        assert antenna_direction_path[-1] == PositionTime(
            position=Position(altitude=-58.827280171790655, azimuth=98.42630806438551),
            time=datetime(year=2023, month=3, day=30, hour=15, minute=0, tzinfo=pytz.UTC)
        )

    def test_get_antenna_direction_path_static_config(self):
        var_initializer = VariableInitializerFromConfig(
                satellites_loader=self.stub_satellites_loader,
                config=self.static_config
        )
        
        antenna_direction_path = var_initializer.get_antenna_direction_path()
        assert antenna_direction_path == [
            PositionTime(
                position=Position(altitude=0.2, azimuth=0.3),
                time=datetime(year=2023, month=3, day=30, hour=10, minute=0, tzinfo=pytz.UTC)
            )
        ]

    def test_get_antenna_direction_path_antenna_position_config(self):
        var_initializer = VariableInitializerFromConfig(
                satellites_loader=self.stub_satellites_loader,
                config=self.antenna_position_config
        )
        
        antenna_direction_path = var_initializer.get_antenna_direction_path()
        assert antenna_direction_path == [
            PositionTime(
                position=Position(altitude=0.0, azimuth=0.1),
                time=datetime(year=2023, month=3, day=30, hour=10, minute=1, tzinfo=pytz.UTC)
            ),
            PositionTime(
                position=Position(altitude=0.1, azimuth=0.2),
                time=datetime(year=2023, month=3, day=30, hour=10, minute=2, tzinfo=pytz.UTC)
            ),
        ]
