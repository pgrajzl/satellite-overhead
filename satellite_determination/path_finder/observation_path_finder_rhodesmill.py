from typing import List, Tuple
from datetime import timedelta
import re

from skyfield.api import load
from skyfield.toposlib import wgs84
from skyfield.starlib import Star

from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.observation_target import ObservationTarget
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.position import Position
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.path_finder.observation_path_finder import ObservationPathFinder


class ObservationPathFinderRhodesMill(ObservationPathFinder):
    '''
    The ObservationPathFinder determines the path the telescope will need to follow to track its target and returns
    a list of altitude, azimuth, and timestamp to represent the telescope's movement. It uses the observation
    target's right ascension and declination to determine this path.
    '''

    def __init__(self, facility: Facility, observation_target: ObservationTarget, time_window: TimeWindow) -> List[PositionTime]:
        self._facility = facility
        self._observation_target = observation_target
        self._time_window = time_window

    def calculate_path(self) -> List[PositionTime]:
        observation_path = []
        observing_location = wgs84.latlon(
            latitude_degrees=self._facility.coordinates.latitude,
            longitude_degrees=self._facility.coordinates.longitude,
            elevation_m=self._facility.elevation
        )

        ts = load.timescale()
        eph = load('de421.bsp')
        earth = eph['earth']

        target_coordinates = Star(
            ra_hours=ObservationPathFinderRhodesMill.right_ascension_to_rhodesmill(self._observation_target),
            dec_degrees=ObservationPathFinderRhodesMill.declination_to_rhodesmill(self._observation_target)
        )
        start_time = self._time_window.begin
        end_time = self._time_window.end

        while start_time <= end_time:
            observing_time = ts.from_datetime(start_time)

            astrometric = (earth + observing_location).at(observing_time).observe(target_coordinates)
            position = astrometric.apparent()
            alt, az, _ = position.altaz()

            point = PositionTime(
                position=Position(altitude=alt.degrees, azimuth=az.degrees),
                time=start_time
            )
            observation_path.append(point)
            start_time += timedelta(minutes=1)

        return observation_path

    @staticmethod
    def _parse_coordinate(coordinate_str: str) -> Tuple[float, float, float]:
        parts = [float(part) for part in re.split('[hdms]', coordinate_str) if part]

        return tuple(parts)

    @staticmethod
    def right_ascension_to_rhodesmill(observation_target: ObservationTarget) -> Tuple[float, float, float]:
        return ObservationPathFinderRhodesMill._parse_coordinate(observation_target.right_ascension)

    @staticmethod
    def declination_to_rhodesmill(observation_target: ObservationTarget) -> Tuple[float, float, float]:
        return ObservationPathFinderRhodesMill._parse_coordinate(observation_target.declination)
