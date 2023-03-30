from satellite_determination.path_finder.observation_path_finder import ObservationPathFinder
from satellite_determination.custom_dataclasses.observation_path import ObservationPath
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.custom_dataclasses.frequency_range import FrequencyRange
from datetime import datetime
from typing import List
from astropy.coordinates import Angle
import filecmp
import os

class TestObservationPathFinder:

    def test(self):
        path = ObservationPathFinder(self._arbitrary_reservation).calculate_path()
        with open ("path_test.txt", "w") as outfile:
            outfile.writelines(str(path))
            outfile.close()
        assert filecmp.cmp('expected_path.txt',
                           'path_test.txt') == 1
        os.remove("path_test.txt")
        #assert path == self._expected_path


    @property
    def _arbitrary_reservation(self) -> Reservation:
        return Reservation(
            facility=Facility(
                point_coordinates=Coordinates(
                    latitude=40,
                    longitude=-121
                ),
                name='HCRO',
                right_ascension='4h42m',
                declination='-38d6m50.8s'
            ),
            time=TimeWindow(
                begin=datetime(year=2023, month=3, day=30, hour=1, minute=0),
                end=datetime(year=2023, month=3, day=30, hour=1, minute=4)
            ),
            frequency=FrequencyRange(
                frequency=130,
                bandwidth=10
            )
        )

    @property
    def _expected_path(self) -> List[ObservationPath]:
        return [
            ObservationPath(
                azimuth=Angle('266d44m39.09228102s'),
                altitude=Angle('-48d39m51.81437374s'),
                time=datetime(year=2023, month=3, day=30, hour=1, minute=0)
            ),
            ObservationPath(
                azimuth=Angle('266d55m57.96379603s'),
                altitude=Angle('-48d49m03.43795986s'),
                time=datetime(year=2023, month=3, day=30, hour=1, minute=1)
            ),
            ObservationPath(
                azimuth=Angle('267d07m18.73122851s'),
                altitude=Angle('-48d58m15.15896219s'),
                time=datetime(year=2023, month=3, day=30, hour=1, minute=2)
            ),
            ObservationPath(
                azimuth=Angle('267d18m41.42221045s'),
                altitude=Angle('-49d07m26.97163597'),
                time=datetime(year=2023, month=3, day=30, hour=1, minute=3)
            ),
            ObservationPath(
                azimuth=Angle('267d30m06.06474439s'),
                altitude=Angle('-49d16m38.87018814s'),
                time=datetime(year=2023, month=3, day=30, hour=1, minute=4)
            )
        ]
