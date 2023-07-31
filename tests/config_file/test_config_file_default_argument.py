import os
import shutil
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
from satellite_determination.utilities import get_default_config_file_filepath, get_script_directory


class TestConfigFileDefaultArgument:
    @pytest.fixture(scope='class')
    def backup_current_default_config_file(self):
        default_filepath = get_default_config_file_filepath()
        backup_filepath = Path(f'{default_filepath}.bak')

        if default_filepath.exists():
            os.rename(default_filepath, backup_filepath)

        yield

        if backup_filepath.exists():
            os.rename(backup_filepath, default_filepath)

    @pytest.fixture(scope='class')
    def config_file(self, backup_current_default_config_file):
        default_filepath = get_default_config_file_filepath()
        os.makedirs(os.path.dirname(default_filepath), exist_ok=True)
        shutil.copyfile(Path(get_script_directory(__file__), 'config_file_standard/arbitrary_config_file_2.config'), default_filepath)

        yield ConfigFile()

        default_filepath.unlink(missing_ok=True)

    def test_reads_inputs_of_provided_config_file_correctly(self, config_file: ConfigFile):
        assert config_file.configuration == Configuration(
            reservation=Reservation(
                facility=Facility(
                    coordinates=Coordinates(latitude=40.8178049,
                                            longitude=-121.4695413),
                    name='ARBITRARY_2',
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
