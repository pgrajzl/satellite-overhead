from sopp.custom_dataclasses.configuration import Configuration
from sopp.custom_dataclasses.observation_target import ObservationTarget
from sopp.custom_dataclasses.facility import Facility
from sopp.custom_dataclasses.coordinates import Coordinates
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.runtime_settings import RuntimeSettings
from sopp.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.custom_dataclasses.position import Position
from sopp.path_finder.observation_path_finder_rhodesmill import ObservationPathFinderRhodesmill
from sopp.path_finder.observation_path_finder import ObservationPathFinder
from sopp.satellites_loader.satellites_loader_from_files import SatellitesLoaderFromFiles
from sopp.config_file_loader.config_file_loader_factory import get_config_file_object
from sopp.config_file_loader.support.config_file_loader_json import ConfigFileLoaderJson
from sopp.config_file_loader.support.config_file_loader_base import ConfigFileLoaderBase
from sopp.satellites_filter.filterer import Filterer
from sopp.utilities import parse_time_and_convert_to_utc

from typing import Optional, List, Type, Union
from pathlib import Path
from datetime import datetime, timedelta


class ConfigurationBuilder:
    def __init__(
        self,
        path_finder_class: Type[ObservationPathFinder] = ObservationPathFinderRhodesmill,
        config_file_loader_class: Type[ConfigFileLoaderBase] = ConfigFileLoaderJson,
    ):
        self._facility: Optional[Facility] = None
        self._time_window: Optional[TimeWindow] = None
        self._frequency_range: Optional[FrequencyRange] = None

        self._path_finder_class = path_finder_class
        self._config_file_loader_class = config_file_loader_class

        self._filterer: Optional[Filterer] = None

        self._observation_target: Optional[ObservationTarget] = None
        self._static_observation_target: Optional[Position] = None
        self._custom_observation_path: Optional[List[PositionTime]] = None

        self._antenna_direction_path: Optional[List[PositionTime]] = None
        self._satellites: Optional[List[Satellite]] = None
        self._reservation: Optional[Reservation] = None
        self._runtime_settings: RuntimeSettings = RuntimeSettings()

    def set_facility(
        self,
        latitude: float,
        longitude: float,
        elevation: float,
        name: str,
        beamwidth: float,
    ) -> 'ConfigurationBuilder':
        self._facility = Facility(
            Coordinates(latitude=latitude, longitude=longitude),
            elevation=elevation,
            beamwidth=beamwidth,
            name=name,
        )
        return self

    def set_frequency_range(self, bandwidth: float, frequency: float):
        self._frequency_range = FrequencyRange(
            bandwidth=bandwidth,
            frequency=frequency,
        )
        return self

    def set_time_window(
        self,
        begin: Union[str, datetime],
        end: Union[str, datetime],
    ) -> 'ConfigurationBuilder':
        self._time_window = TimeWindow(
            begin = parse_time_and_convert_to_utc(begin),
            end = parse_time_and_convert_to_utc(end)
        )
        return self

    def set_observation_target(
        self,
        declination: Optional[str] = None,
        right_ascension: Optional[str] = None,
        altitude: Optional[float] = None,
        azimuth: Optional[float] = None,
        custom_path: Optional[List[PositionTime]] = None
    ) -> 'ConfigurationBuilder':
        if custom_path:
            self._custom_observation_path = custom_path
        elif altitude is not None and azimuth is not None:
            self._static_observation_target = Position(
                altitude=altitude,
                azimuth=azimuth
            )
        elif declination is not None and right_ascension is not None:
            self._observation_target = ObservationTarget(
                declination=declination,
                right_ascension=right_ascension,
            )
        else:
            raise ValueError(
                "Specify at least one way to set the observation target. "
                "Valid combinations are: "
                "1. right_ascension and declination, "
                "2. altitude and azimuth, or "
                "3. custom_path."
            )
        return self

    def set_satellites(
        self,
        tle_file: str,
        frequency_file: Optional[str] = None
    ) -> 'ConfigurationBuilder':
        self._satellites = SatellitesLoaderFromFiles(
            tle_file=tle_file,
            frequency_file=frequency_file,
        ).load_satellites()
        return self

    def set_runtime_settings(
        self,
        concurrency_level: int,
        time_continuity_resolution: int
    ) -> 'ConfigurationBuilder':
        self._runtime_settings = RuntimeSettings(
            concurrency_level=concurrency_level,
            time_continuity_resolution=time_continuity_resolution,
        )
        return self

    def set_from_config_file(self, config_file: Optional[Path] = None) -> 'ConfigurationBuilder':
        config = self._config_file_loader_class(filepath=config_file).configuration
        self._frequency_range = config.reservation.frequency
        self._facility = config.reservation.facility
        self._time_window = config.reservation.time
        self._runtime_settings = config.runtime_settings

        if config.antenna_position_times:
            self._custom_observation_path = config.antenna_position_times
        elif config.static_antenna_position:
            self._static_observation_target = config.static_antenna_position
        else:
            self._observation_target = config.observation_target
        return self

    def set_satellites_filter(self, filterer: Type[Filterer]) -> 'ConfigurationBuilder':
        self._filterer = filterer
        return self

    def _filter_satellites(self):
        if self._filterer:
            self._satellites = self._filterer.apply_filters(self._satellites)

    def _build_reservation(self):
        self._reservation = Reservation(
            facility=self._facility,
            time=self._time_window,
            frequency=self._frequency_range
        )

    def _build_antenna_direction_path(self) -> 'ConfigurationBuilder':
        if self._custom_observation_path:
            self._antenna_direction_path = self._custom_observation_path
        elif self._static_observation_target:
            self._antenna_direction_path = [
                PositionTime(
                    position=self._static_observation_target,
                    time=self._time_window.begin
                )
            ]
        elif self._observation_target:
            self._antenna_direction_path = self._path_finder_class(
                self._facility,
                self._observation_target,
                self._time_window
            ).calculate_path()

    def build(self) -> 'Configuration':
        if not (
            all([self._facility, self._time_window, self._frequency_range, self._satellites])
        ):
            raise ValueError(
                "Incomplete configuration. Ensure that the following are called: "
                "set_facility, set_time_window, set_frequency_range, "
                "set_satellites, or set_from_config_file."
            )

        self._filter_satellites()
        self._build_antenna_direction_path()
        self._build_reservation()

        configuration = Configuration(
            reservation=self._reservation,
            satellites=self._satellites,
            antenna_direction_path=self._antenna_direction_path,
            runtime_settings=self._runtime_settings
        )
        return configuration
