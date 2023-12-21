import datetime
import pytz

from astropy.coordinates import EarthLocation, SkyCoord, AltAz
from astropy.time import Time
from astropy import units
from typing import List
from datetime import timedelta

from sopp.config_file_loader.support.utilities import TIME_FORMAT
from sopp.custom_dataclasses.facility import Facility
from sopp.custom_dataclasses.observation_target import ObservationTarget
from sopp.custom_dataclasses.position import Position
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.path_finder.observation_path_finder import ObservationPathFinder
from sopp.custom_dataclasses.time_window import TimeWindow


class ObservationPathFinderAstropy(ObservationPathFinder):
    def __init__(self, facility: Facility, observation_target: ObservationTarget, time_window: TimeWindow) -> List[PositionTime]:
        self._facility = facility
        self._observation_target = observation_target
        self._time_window = time_window

    def calculate_path(self) -> List[PositionTime]:
        observation_path = []
        observing_location = EarthLocation(lat=str(self._facility.coordinates.latitude),
                                           lon=str(self._facility.coordinates.longitude),
                                           height=self._facility.elevation * units.m)
        target_coordinates = SkyCoord(self._observation_target.right_ascension, self._observation_target.declination)
        start_time = self._get_time_as_astropy_time(self._time_window.begin)
        end_time = self._get_time_as_astropy_time(self._time_window.end)
        while start_time <= end_time:
            observing_time = Time(str(start_time))
            altitude_azimuth = AltAz(location=observing_location, obstime=observing_time)
            point_coord = target_coordinates.transform_to(altitude_azimuth)
            point = PositionTime(
                position=Position(altitude=point_coord.alt.degree, azimuth=point_coord.az.degree),
                time=start_time.datetime.replace(tzinfo=pytz.UTC)
            )
            observation_path.append(point)
            start_time += timedelta(minutes=1)
        return observation_path

    @staticmethod
    def _get_time_as_astropy_time(time: datetime) -> Time:
        return Time(time.strftime(TIME_FORMAT), scale='utc')
