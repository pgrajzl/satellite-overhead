from datetime import datetime
from pathlib import Path

import pytest
import pytz

from satellite_determination.config_file import ConfigFile
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.utilities import get_script_directory


class TestConfigFileProvidedArgument:
    @pytest.fixture
    def config_file(self) -> ConfigFile:
        return ConfigFile(filepath=Path(get_script_directory(__file__), 'arbitrary_config_file.config'))

    def test_reads_inputs_of_provided_config_file_correctly(self, config_file):
        assert config_file.reservation == Reservation(
            facility=Facility(
                right_ascension='4h42m',
                point_coordinates=Coordinates(latitude=40.8178049,
                                              longitude=-121.4695413),
                name='ARBITRARY_1',
                declination='-38d6m50.8s',
            ),
            time=TimeWindow(begin=datetime(year=2023, month=3, day=30, hour=10, tzinfo=pytz.UTC),
                            end=datetime(year=2023, month=3, day=30, hour=11, tzinfo=pytz.UTC)),
            frequency=FrequencyRange(
                frequency=135,
                bandwidth=10
            )
        )

    def test_reads_search_window_inputs_correctly(self, config_file):
        assert config_file.search_window == TimeWindow(begin=datetime(year=2023, month=3, day=30, hour=11, tzinfo=pytz.UTC),
                                                       end=datetime(year=2023, month=3, day=30, hour=12, tzinfo=pytz.UTC))
