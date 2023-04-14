from astropy.coordinates import EarthLocation, SkyCoord, Angle, AltAz
from astropy.time import Time
from astropy import units as u
from typing import List
from datetime import timedelta
from satellite_determination.custom_dataclasses.observation_path import ObservationPath
from satellite_determination.custom_dataclasses.reservation import Reservation
import pytz

class ObservationPathFinder:

    def __init__(self, reservation: Reservation, start_str: str, end_str: str) -> List[ObservationPath]:
        self._reservation = reservation
        self._start_time_str = start_str
        self._end_time_str = end_str

    def calculate_path(self) -> List[ObservationPath]:
        observation_path = []
        observing_location = EarthLocation(lat=str(self._reservation.facility.point_coordinates.latitude), lon=str(self._reservation.facility.point_coordinates.longitude), height=self._reservation.facility.height * u.m)
        target_coordinates = SkyCoord(self._reservation.facility.right_ascension, self._reservation.facility.declination)
        #start_time = self._reservation.time.begin
        #end_time = self._reservation.time.end
        start_time = Time(self._start_time_str, scale='utc')
        end_time = Time(self._end_time_str, scale='utc')
        while start_time <= end_time:
            observing_time = Time(str(start_time))
            altitude_azimuth = AltAz(location=observing_location, obstime=observing_time)
            point_coord = target_coordinates.transform_to(altitude_azimuth)
            point = ObservationPath(
                altitude=Angle(point_coord.alt),
                azimuth=Angle(point_coord.az),
                time=start_time.datetime.replace(tzinfo=pytz.UTC)
            )
            observation_path.append(point)
            start_time+=timedelta(minutes=1)
        return observation_path
