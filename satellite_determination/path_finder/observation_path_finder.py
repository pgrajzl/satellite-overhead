from astropy.coordinates import EarthLocation, SkyCoord, Angle, AltAz
from astropy.time import Time
from astropy import units as u
from typing import List
from datetime import timedelta
from satellite_determination.custom_dataclasses.observation_path import ObservationPath
from satellite_determination.custom_dataclasses.reservation import Reservation

class ObservationPathFinder:

    def __init__(self, reservation: Reservation) -> List[ObservationPath]:
        self._reservation = reservation

    def calculate_path(self) -> List[ObservationPath]:
        observation_path = []
        observing_location = EarthLocation(lat='52.2532', lon='351.63910339111703', height=100*u.m)
        target_coordinates = SkyCoord(self._reservation.facility.right_ascension, self._reservation.facility.declination)
        start_time = self._reservation.time.begin
        end_time = self._reservation.time.end
        while start_time <= end_time:
            observing_time = Time(str(start_time))
            altitude_azimuth = AltAz(location=observing_location, obstime=observing_time)
            point_coord = target_coordinates.transform_to(altitude_azimuth)
            print(Angle(point_coord.alt))
            print(Angle(point_coord.az))
            point = ObservationPath(
                altitude=Angle(point_coord.alt),
                azimuth=Angle(point_coord.az),
                time=start_time
            )
            observation_path.append(point)
            start_time+=timedelta(minutes=1)
        return observation_path
