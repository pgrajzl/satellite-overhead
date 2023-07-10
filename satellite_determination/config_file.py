from configparser import ConfigParser
from datetime import datetime
from functools import cached_property
from pathlib import Path

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


class ConfigFile:
    def __init__(self, filepath: Path = get_default_config_file_filepath()):
        self._filepath = filepath

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
        start_datetime = self._read_datetime_as_utc(configuration['StartTimeUTC'])
        end_datetime_str = self._read_datetime_as_utc(configuration['EndTimeUTC'])
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

    @staticmethod
    def _read_datetime_as_utc(string_value: str) -> datetime:
        without_timezone = datetime.strptime(string_value, TIME_FORMAT)
        return convert_datetime_to_utc(without_timezone)

    @cached_property
    def _observation_target(self) -> ObservationTarget:
        observation_target_parameters = self._config_object['OBSERVATION TARGET']
        return ObservationTarget(
            declination=observation_target_parameters['Declination'],
            right_ascension=observation_target_parameters['Right Ascension']
        )

    @cached_property
    def _static_antenna_position(self) -> Position:
        configuration = self._config_object['STATIC ANTENNA POSITION']
        return Position(
            altitude=float(configuration['Altitude']),
            azimuth=float(configuration['Azimuth'])
        )

    @cached_property
    def _config_object(self) -> dict:
        config_object = ConfigParser()
        config_object.read(self._filepath)
        return config_object
