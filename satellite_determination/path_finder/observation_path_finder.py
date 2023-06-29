import datetime

from astropy.coordinates import EarthLocation, SkyCoord, AltAz
from astropy.time import Time
from astropy import units
from typing import List
from datetime import timedelta

from satellite_determination.config_file import TIME_FORMAT
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.position_time import PositionTime
import pytz

from satellite_determination.custom_dataclasses.time_window import TimeWindow


class ObservationPathFinder:
    '''
    The ObservationPathFinder determines the path the telescope will need to follow to track its target and returns
    a list of altitude, azimuth, and timestamp to represent the telescope's movement. It uses the observation
    target's right ascension and declination to determine this path.
    '''

    def __init__(self, facility: Facility, time_window: TimeWindow) -> List[PositionTime]:
        self._facility = facility
        self._time_window = time_window

    def calculate_path(self) -> List[PositionTime]:
        observation_path = []
        observing_location = EarthLocation(lat=str(self._facility.coordinates.latitude),
                                           lon=str(self._facility.coordinates.longitude),
                                           height=self._facility.height * units.m)
        target_coordinates = SkyCoord(self._facility.right_ascension, self._facility.declination)
        start_time = self._get_time_as_astropy_time(self._time_window.begin)
        end_time = self._get_time_as_astropy_time(self._time_window.end)
        while start_time <= end_time:
            observing_time = Time(str(start_time))
            altitude_azimuth = AltAz(location=observing_location, obstime=observing_time)
            point_coord = target_coordinates.transform_to(altitude_azimuth)
            point = PositionTime(
                altitude=point_coord.alt.degree,
                azimuth=point_coord.az.degree,
                time=start_time.datetime.replace(tzinfo=pytz.UTC)
            )
            observation_path.append(point)
            start_time += timedelta(minutes=1)
        return observation_path

    @staticmethod
    def _get_time_as_astropy_time(time: datetime) -> Time:
        return Time(time.strftime(TIME_FORMAT), scale='utc')
