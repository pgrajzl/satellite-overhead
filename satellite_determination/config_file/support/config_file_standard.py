from configparser import ConfigParser
from functools import cached_property

from satellite_determination.config_file.support.config_file_base import ConfigFileBase
from satellite_determination.custom_dataclasses.configuration import Configuration
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.observation_target import ObservationTarget
from satellite_determination.custom_dataclasses.position import Position
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.utilities import read_datetime_string_as_utc


class ConfigFileStandard(ConfigFileBase):
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
        start_datetime = read_datetime_string_as_utc(configuration['StartTimeUTC'])
        end_datetime_str = read_datetime_string_as_utc(configuration['EndTimeUTC'])
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
