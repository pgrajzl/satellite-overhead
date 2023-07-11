from datetime import datetime
from pathlib import Path

import pytest
import pytz

from satellite_determination.config_file import ConfigFile
from satellite_determination.custom_dataclasses.configuration import Configuration
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.observation_target import ObservationTarget
from satellite_determination.custom_dataclasses.position import Position
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.utilities import get_script_directory


class TestConfigFileProvidedArgument:
    def test_reads_inputs_of_provided_config_file_correctly(self):
        config_file = self._get_config_file_object('arbitrary_config_file.config')
        assert config_file.configuration == Configuration(
            reservation=Reservation(
                facility=Facility(
                    coordinates=Coordinates(latitude=40.8178049,
                                            longitude=-121.4695413),
                    name='ARBITRARY_1',
                ),
                time=TimeWindow(begin=datetime(year=2023, month=3, day=30, hour=10, tzinfo=pytz.UTC),
                                end=datetime(year=2023, month=3, day=30, hour=11, tzinfo=pytz.UTC)),
                frequency=FrequencyRange(
                    frequency=135,
                    bandwidth=10
                )
            ),
            observation_target=ObservationTarget(declination='-38d6m50.8s', right_ascension='4h42m'),
            static_antenna_position=Position(altitude=.2, azimuth=.3)
        )

    def test_observation_target_is_optional(self):
        config_file = self._get_config_file_object('arbitrary_config_file_no_observation_target.config')
        assert config_file.configuration.observation_target is None
        assert config_file.configuration.reservation is not None
        assert config_file.configuration.static_antenna_position is not None

    def test_error_is_returned_if_partial_observation_target(self):
        config_file = self._get_config_file_object('arbitrary_config_file_partial_observation_target.config')
        with pytest.raises(KeyError):
            _ = config_file.configuration

    def test_static_antenna_position_is_optional(self):
        config_file = self._get_config_file_object('arbitrary_config_file_no_static_antenna_position.config')
        assert config_file.configuration.static_antenna_position is None
        assert config_file.configuration.observation_target is not None
        assert config_file.configuration.reservation is not None

    def test_error_is_returned_if_partial_static_antenna_position(self):
        config_file = self._get_config_file_object('arbitrary_config_file_partial_static_antenna_position.config')
        with pytest.raises(KeyError):
            _ = config_file.configuration

    @staticmethod
    def _get_config_file_object(config_filename: str) -> ConfigFile:
        return ConfigFile(filepath=Path(get_script_directory(__file__), config_filename))
