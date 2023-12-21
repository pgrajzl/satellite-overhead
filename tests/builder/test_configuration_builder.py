import pytest

from datetime import datetime
import pytz

from sopp.builder.configuration_builder import ConfigurationBuilder
from sopp.custom_dataclasses.configuration import Configuration
from sopp.custom_dataclasses.configuration_file import ConfigurationFile
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.facility import Facility
from sopp.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from sopp.custom_dataclasses.coordinates import Coordinates
from sopp.custom_dataclasses.observation_target import ObservationTarget
from sopp.custom_dataclasses.position import Position
from sopp.custom_dataclasses.runtime_settings import RuntimeSettings
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.custom_dataclasses.satellite.satellite import Satellite
from sopp.custom_dataclasses.position_time import PositionTime


class TestConfigurationBuilder:
    def test_set_facility(self):
        builder = ConfigurationBuilder()
        builder.set_facility(
            latitude=40,
            longitude=-121,
            elevation=100,
            name='HCRO',
            beamwidth=3,
            bandwidth=10,
            frequency=135,
        )
        assert builder._facility == Facility(
            Coordinates(latitude=40, longitude=-121),
            elevation=100,
            beamwidth=3,
            name='HCRO',
        )
        assert builder._frequency_range == FrequencyRange(
            bandwidth=10,
            frequency=135,
        )

    def test_set_observation_target_error(self):
        builder = ConfigurationBuilder()

        with pytest.raises(ValueError) as _:
            builder.set_observation_target(altitude=1)

    def test_set_observation_target(self):
        builder = ConfigurationBuilder()
        builder.set_observation_target(
            declination='1d1m1s',
            right_ascension='1h1m1s',
        )
        assert builder._observation_target == ObservationTarget(
            declination='1d1m1s',
            right_ascension='1h1m1s',
        )

    def test_set_observation_target_static(self):
        builder = ConfigurationBuilder()
        builder.set_observation_target(altitude=1, azimuth=1)

        assert builder._static_observation_target == Position(
            altitude=1,
            azimuth=1,
        )

    def test_set_observation_target_custom(self):
        builder = ConfigurationBuilder()
        builder.set_observation_target(custom_path=expected_position_time())

        assert builder._custom_observation_path == expected_position_time()

    def test_set_runtime_settings(self):
        builder = ConfigurationBuilder()
        builder.set_runtime_settings(
            concurrency_level=1,
            time_continuity_resolution=1
        )

        assert builder._runtime_settings == RuntimeSettings(
            concurrency_level=1,
            time_continuity_resolution=1,
        )

    def test_set_time_window(self):
        builder = ConfigurationBuilder()
        builder.set_time_window(
            begin='2023-11-15T08:00:00.0',
            end='2023-11-15T08:30:00.0',
        )

        assert builder._time_window == TimeWindow(
            begin=datetime(2023, 11, 15, 8, 0, tzinfo=pytz.UTC),
            end=datetime(2023, 11, 15, 8, 30, tzinfo=pytz.UTC),
        )

    def test_set_satellites(self, monkeypatch):
        mock_satellite_loader(monkeypatch)
        builder = ConfigurationBuilder()
        builder.set_satellites("/mock/tle", 'mock/frequency')

        assert builder._satellites == [ Satellite(name='TestSatellite') ]

    def test_filter_satellties_by_frequency_false(self):
        builder = ConfigurationBuilder()
        expected = [ Satellite(name='ToFilterSatellite'), Satellite(name='Satellite') ]
        builder._satellites = expected
        builder.set_filter_satellites(False)
        builder._filter_satellites_by_frequency()

        assert builder._satellites == expected

    def test_filter_satellties_by_frequency_true(self, monkeypatch):
        def mock_frequency_filter(mock):
            return [ Satellite(name='Satellite') ]

        monkeypatch.setattr(
            'sopp.frequency_filter.frequency_filter.FrequencyFilter.filter_frequencies',
            mock_frequency_filter
        )
        builder = ConfigurationBuilder()
        builder._filter_satellites_by_frequency()

        assert builder._satellites == [ Satellite(name='Satellite') ]

    def test_build_antenna_direction_path_target(self):
        builder = ConfigurationBuilder(path_finder_class=StubPathFinder)
        builder._build_antenna_direction_path()

        assert builder._antenna_direction_path == [expected_position_time()]

    def test_build_antenna_direction_path_static(self):
        builder = ConfigurationBuilder()
        builder._static_observation_target = expected_position_time().position
        builder.set_time_window(
            begin='2023-11-15T08:00:00.0',
            end='2023-11-15T08:30:00.0',
        )
        builder._build_antenna_direction_path()

        assert builder._antenna_direction_path == [expected_position_time()]

    def test_build_antenna_direction_path_custom(self):
        builder = ConfigurationBuilder()
        builder._custom_observation_path = [expected_position_time()]
        builder._build_antenna_direction_path()

        assert builder._antenna_direction_path == [expected_position_time()]

    def test_build_error(self):
        builder = ConfigurationBuilder()

        with pytest.raises(ValueError) as _:
            builder.build()

    def test_build_from_config_file(self, monkeypatch):
        mock_satellite_loader(monkeypatch)
        configuration = (
            ConfigurationBuilder(
                config_file_loader_class=StubConfigFileLoader,
                path_finder_class=StubPathFinder,
            )
            .set_from_config_file(config_file='mock/path')
            .set_satellites(tle_file='./path/satellites.tle')
            .build()
        )

        assert configuration == Configuration(
            reservation=expected_reservation(),
            runtime_settings=RuntimeSettings(),
            antenna_direction_path=[expected_position_time()],
            satellites=[Satellite(name='TestSatellite')]
        )

    def test_build(self, monkeypatch):
        mock_satellite_loader(monkeypatch)
        configuration = (
            ConfigurationBuilder(path_finder_class=StubPathFinder)
            .set_facility(
                latitude=1,
                longitude=-1,
                elevation=1,
                name='HCRO',
                beamwidth=3,
                bandwidth=10,
                frequency=135
            )
            .set_time_window(
                begin='2023-11-15T08:00:00.0',
                end='2023-11-15T08:30:00.0'
            )
            .set_observation_target(
                declination='1d1m1s',
                right_ascension='1h1m1s'
            )
            .set_satellites(tle_file='./path/satellites.tle')
            .build()
        )

        assert configuration == Configuration(
            reservation=expected_reservation(),
            runtime_settings=RuntimeSettings(),
            antenna_direction_path=[expected_position_time()],
            satellites=[Satellite(name='TestSatellite')]
        )

class StubConfigFileLoader:
    def __init__(self, filepath):
        self.configuration = ConfigurationFile(
            reservation=expected_reservation(),
            observation_target='target',
        )

class StubPathFinder:
    def __init__(self, a, b, c):
        pass
    def calculate_path(self):
        return [expected_position_time()]

def mock_satellite_loader(monkeypatch):
    def mock(tle_file, frequency_file=None):
        return [ Satellite(name='TestSatellite') ]

    monkeypatch.setattr(
        'sopp.satellites_loader.satellites_loader_from_files.SatellitesLoaderFromFiles.load_satellites',
        mock
    )

def expected_position_time():
    return PositionTime(
        position=Position(altitude=.0, azimuth=.1),
        time=datetime(2023, 11, 15, 8, 0, tzinfo=pytz.UTC),
    )

def expected_reservation():
    return Reservation(
        facility=Facility(
            coordinates=Coordinates(longitude=-1, latitude=1),
            beamwidth=3,
            elevation=1,
            name='HCRO'
        ),
        time=TimeWindow(
            begin=datetime(2023, 11, 15, 8, 0, tzinfo=pytz.UTC),
            end=datetime(2023, 11, 15, 8, 30, tzinfo=pytz.UTC),
        ),
        frequency=FrequencyRange(
            bandwidth=10,
            frequency=135,
        )
    )
