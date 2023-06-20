from astropy.coordinates import EarthLocation, SkyCoord, Angle, AltAz
from astropy.time import Time
from astropy import units as u
from typing import List
from datetime import timedelta
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.reservation import Reservation
import pytz

class ObservationPathFinder:
    '''
    The PathFinder determines the path the telescope will need to follow to track its target and returns
    a list of altitude, azimuth, and timestamp to represent the telescope's movement. It uses the observation
    target's right ascension and declination to determine this path.
    '''

    def __init__(self, reservation: Reservation, start_str: str, end_str: str) -> List[PositionTime]:
        self._reservation = reservation
        self._start_time_str = start_str
        self._end_time_str = end_str

    def calculate_path(self) -> List[PositionTime]:
        observation_path = []
        observing_location = EarthLocation(lat=str(self._reservation.facility.coordinates.latitude), lon=str(self._reservation.facility.coordinates.longitude), height=self._reservation.facility.height * u.m)
        target_coordinates = SkyCoord(self._reservation.facility.right_ascension, self._reservation.facility.declination)
        start_time = Time(self._start_time_str, scale='utc')
        end_time = Time(self._end_time_str, scale='utc')
        while start_time <= end_time:
            observing_time = Time(str(start_time))
            altitude_azimuth = AltAz(location=observing_location, obstime=observing_time)
            point_coord = target_coordinates.transform_to(altitude_azimuth)
            point = PositionTime(
                altitude=Angle(point_coord.alt),
                azimuth=Angle(point_coord.az),
                time=start_time.datetime.replace(tzinfo=pytz.UTC)
            )
            observation_path.append(point)
            start_time+=timedelta(minutes=1)
        return observation_path