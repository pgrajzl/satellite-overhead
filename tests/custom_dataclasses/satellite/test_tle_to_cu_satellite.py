from pathlib import Path

from satellite_determination.custom_dataclasses.satellite.international_designator import InternationalDesignator
from satellite_determination.custom_dataclasses.satellite.mean_motion import MeanMotion
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.satellite.tle_information import TleInformation
from tests.utilities import get_script_directory


class TestTleToSatelliteCu:
    def test(self):
        tle_file = Path(get_script_directory(__file__), 'international_space_station_tle.tle')
        satellite = Satellite.from_tle_file(filepath=tle_file)
        assert satellite == Satellite(
            name='ISS (ZARYA)',
            tle_information=TleInformation(
                argument_of_perigee=0.3083420829620822,
                drag_coefficient=3.8792e-05,
                eccentricity=0.0007417,
                epoch_days=25545.69339541,
                inclination=0.9013560935706996,
                international_designator=InternationalDesignator(
                    year=98,
                    launch_number=67,
                    launch_piece='A'
                ),
                mean_anomaly=1.4946964807494398,
                mean_motion=MeanMotion(
                    first_derivative=5.3450708342326346e-11,
                    second_derivative=0.0,
                    value=0.06763602333248933
                ),
                revolution_number=20248,
                right_ascension_of_ascending_node=3.686137125541276,
                satellite_number=25544
            )
        )
