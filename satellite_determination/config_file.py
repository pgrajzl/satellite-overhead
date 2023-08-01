import json
from abc import ABC, abstractmethod
from configparser import ConfigParser
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Optional

from satellite_determination.custom_dataclasses.configuration import Configuration
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.observation_target import ObservationTarget
from satellite_determination.custom_dataclasses.position import Position
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.utilities import convert_datetime_to_utc, get_default_config_file_filepath

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


def read_datetime_as_utc(string_value: str) -> datetime:
    without_timezone = datetime.strptime(string_value, TIME_FORMAT)
    return convert_datetime_to_utc(without_timezone)


class ConfigFileBase(ABC):
    def __init__(self, filepath: Path):
        self._filepath = filepath

    @cached_property
    @abstractmethod
    def configuration(self) -> Configuration:
        pass

    @classmethod
    @abstractmethod
    def filename_extension(cls) -> str:
        pass


class ConfigFileJson(ConfigFileBase):
    @cached_property
    def configuration(self) -> Configuration:
        return Configuration(
            reservation=self._reservation,
            observation_target=self._observation_target,
            static_antenna_position=self._static_antenna_position
        )

    @cached_property
    def _reservation(self) -> Reservation:
        configuration = self._config_object['reservation']
        start_datetime = read_datetime_as_utc(configuration['startTimeUtc'])
        end_datetime_str = read_datetime_as_utc(configuration['endTimeUtc'])
        return Reservation(
            facility=Facility(
                coordinates=Coordinates(latitude=configuration['latitude'],
                                        longitude=configuration['longitude']),
                name=configuration['name'],
            ),
            time=TimeWindow(begin=start_datetime, end=end_datetime_str),
            frequency=FrequencyRange(
                frequency=configuration['frequency'],
                bandwidth=configuration['bandwidth']
            )
        )

    @cached_property
    def _observation_target(self) -> ObservationTarget:
        configuration = self._config_object['observationTarget'] \
            if 'observationTarget' in self._config_object \
            else None
        return configuration and ObservationTarget(
            declination=configuration['declination'],
            right_ascension=configuration['rightAscension']
        )

    @cached_property
    def _static_antenna_position(self) -> Position:
        configuration = self._config_object['staticAntennaPosition'] \
            if 'staticAntennaPosition' in self._config_object \
            else None
        return configuration and Position(
            altitude=configuration['altitude'],
            azimuth=configuration['azimuth']
        )

    @cached_property
    def _config_object(self) -> dict:
        with open(self._filepath, 'r') as f:
            return json.load(f)

    @classmethod
    def filename_extension(cls) -> str:
        return '.json'


def get_config_file_object(config_filepath: Optional[Path] = None) -> ConfigFileBase:
    config_filepath = config_filepath or get_default_config_file_filepath()
    for config_class in (ConfigFile, ConfigFileJson):
        if config_class.filename_extension() in str(config_filepath):
            return config_class(filepath=config_filepath)


class ConfigFile(ConfigFileBase):
    @cached_property
    def configuration(self) -> Configuration:
        return Configuration(
            reservation=self._reservation,
            observation_target=self._observation_target,
            static_antenna_position=self._static_antenna_position
        )

    @cached_property
    def _reservation(self) -> Reservation:
        configuration = self._config_object['RESERVATION']
        start_datetime = read_datetime_as_utc(configuration['StartTimeUTC'])
        end_datetime_str = read_datetime_as_utc(configuration['EndTimeUTC'])
        return Reservation(
            facility=Facility(
                coordinates=Coordinates(latitude=float(configuration['Latitude']),
                                        longitude=float(configuration['Longitude'])),
                name=configuration['Name'],
            ),
            time=TimeWindow(begin=start_datetime, end=end_datetime_str),
            frequency=FrequencyRange(
                frequency=float(configuration['Frequency']),
                bandwidth=float(configuration['Bandwidth'])
            )
        )

    @cached_property
    def _observation_target(self) -> ObservationTarget:
        configuration = self._config_object['OBSERVATION TARGET'] \
            if 'OBSERVATION TARGET' in self._config_object \
            else None
        return configuration and ObservationTarget(
            declination=configuration['Declination'],
            right_ascension=configuration['Right Ascension']
        )

    @cached_property
    def _static_antenna_position(self) -> Position:
        configuration = self._config_object['STATIC ANTENNA POSITION'] \
            if 'STATIC ANTENNA POSITION' in self._config_object \
            else None
        return configuration and Position(
            altitude=float(configuration['Altitude']),
            azimuth=float(configuration['Azimuth'])
        )

    @cached_property
    def _config_object(self) -> dict:
        config_object = ConfigParser()
        config_object.read(self._filepath)
        return config_object

    @classmethod
    def filename_extension(cls) -> str:
        return '.config'
