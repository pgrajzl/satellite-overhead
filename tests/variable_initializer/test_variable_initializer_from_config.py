from datetime import datetime

import os
import pytest
import pytz

from satellite_determination.configuration_loader.configuration_loader_config_file import ConfigurationLoaderConfigFile
from satellite_determination.custom_dataclasses.configuration import Configuration
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.custom_dataclasses.observation_target import ObservationTarget
from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.position import Position
from satellite_determination.custom_dataclasses.position_time import PositionTime


class TestConfigurationLoaderConfigFile:
    @pytest.fixture(scope='class')
    def common_config(self):
        return Configuration(
            reservation=Reservation(
                facility=Facility(
                    coordinates=Coordinates(latitude=40.8178049, longitude=-121.4695413),
                    beamwidth=3,
                    elevation=0,
                    height=100,
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

    @pytest.fixture
    def observation_config(self, common_config):
        config = common_config
        config.observation_target = ObservationTarget(
            declination='-38d6m50.8s',
            right_ascension='4h42m'
        )
        return config

    @pytest.fixture
    def static_config(self, common_config):
        config = common_config
        config.static_antenna_position = Position(altitude=.2, azimuth=.3)
        return config

    @pytest.fixture
    def antenna_position_config(self, common_config):
        config = common_config
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

    def test_get_reservation(self, observation_config):
        config_loader = ConfigurationLoaderConfigFile(config_file=observation_config)
        
        reservation = config_loader.get_reservation()
        assert isinstance(reservation, Reservation)
        
    def test_get_satellite_list(self, observation_config):
        config_loader = ConfigurationLoaderConfigFile(config_file=observation_config)
        
        test_script_directory = os.path.dirname(os.path.abspath(__file__))

        tle_file = os.path.join(test_script_directory, 'satellites.tle')
        frequency_file = os.path.join(test_script_directory, 'satellite_frequencies.csv')

        satellites = config_loader.get_satellite_list(tle_file=tle_file, frequency_file=frequency_file)
        assert isinstance(satellites, list)
        assert len(satellites) > 0
        

    @pytest.mark.parametrize('config', ['observation_config', 'static_config', 'antenna_position_config'])
    def test_get_antenna_direction_path(self, config, request):
        config = request.getfixturevalue(config)
        config_loader = ConfigurationLoaderConfigFile(config_file=config)
        
        antenna_direction_path = config_loader.get_antenna_direction_path()
        assert isinstance(antenna_direction_path, list)
        assert len(antenna_direction_path) > 0
