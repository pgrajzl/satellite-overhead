from pathlib import Path

from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from tests.custom_dataclasses.satellite.utilities import expected_international_space_station_tle_as_satellite_cu
from tests.utilities import get_script_directory


class TestTleToSatelliteCu:
    def test_single_satellite(self):
        tle_file = Path(get_script_directory(__file__), 'international_space_station_tle.tle')
        satellite = Satellite.from_tle_file(filepath=tle_file)
        assert satellite == [self._expected_satellite_first]

    def test_multiple_satellites(self):
        tle_file = Path(get_script_directory(__file__), 'international_space_station_tle_multiple.tle')
        satellite = Satellite.from_tle_file(filepath=tle_file)
        assert satellite == [self._expected_satellite_first, self._expected_satellite_second]

    @property
    def _expected_satellite_second(self) -> Satellite:
        satellite = self._expected_satellite_first
        satellite.name = 'FAKE ISS (ZARYA) 2'
        satellite.tle_information.international_designator.launch_piece = 'AB'
        return satellite

    @property
    def _expected_satellite_first(self) -> Satellite:
        return expected_international_space_station_tle_as_satellite_cu()
