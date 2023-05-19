from configparser import ConfigParser, SectionProxy
from datetime import datetime
from functools import cached_property
from pathlib import Path

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.utilities import convert_datetime_to_utc, get_default_config_file_filepath


TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


class ConfigFile:
    def __init__(self, filepath: Path = get_default_config_file_filepath()):
        self._filepath = filepath

    @property
    def reservation(self) -> Reservation:
        start_datetime = self._read_datetime_as_utc('StartTimeUTC')
        end_datetime_str = self._read_datetime_as_utc('EndTimeUTC')
        return Reservation(
            facility=Facility(
                right_ascension=self._reservation_parameters['RightAscension'],
                point_coordinates=Coordinates(latitude=float(self._reservation_parameters['Latitude']),
                                              longitude=float(self._reservation_parameters['Longitude'])),
                name=self._reservation_parameters['Name'],
                declination=self._reservation_parameters['Declination'],
            ),
            time=TimeWindow(begin=start_datetime, end=end_datetime_str),
            frequency=FrequencyRange(
                frequency=float(self._reservation_parameters['Frequency']),
                bandwidth=float(self._reservation_parameters['Bandwidth'])
            )
        )

    @property
    def search_window(self) -> TimeWindow:
        search_window_start = self._read_datetime_as_utc('SearchWindowStart')
        search_window_end = self._read_datetime_as_utc('SearchWindowEnd')
        return TimeWindow(begin=search_window_start, end=search_window_end)

    def _read_datetime_as_utc(self, key: str) -> datetime:
        string_value = self._reservation_parameters[key]
        without_timezone = datetime.strptime(string_value, TIME_FORMAT)
        return convert_datetime_to_utc(without_timezone)

    @cached_property
    def _reservation_parameters(self) -> SectionProxy:
        config_object = ConfigParser()
        config_object.read(self._filepath)
        return config_object['RESERVATION']
