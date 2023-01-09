import pickle
import re
import types
from pathlib import Path

from satellite_determination.ListOfSatellites import loadSatellites
from satellite_determination.dataclasses.satellite import Satellite
from tests.utilities import get_script_directory


class TestSatelliteToRhodesMill:
    def test_satellite_can_translate_to_rhodesmill(self):
        self.given_a_cu_satellite_with_international_space_station_properties()
        self.given_a_rhodesmill_satellite_loaded_from_the_international_space_station_tle()
        self.when_the_cu_satellite_is_converted_into_rhodesmill()
        self.then_the_satellites_should_match()
        assert self._models_match() and self._non_model_properties_match()

    def given_a_cu_satellite_with_international_space_station_properties(self) -> None:
        self._cu_satellite = Satellite(
            name='ISS (ZARYA)',
            catalog_number='25544',
            classification='U',
            international_designator_year='98',
            international_designator_launch_number='067',
            international_designator_launch_piece='A',
            epoch_year='08',
            epoch_day='264.51782528',
            mean_motion_first_derivative='-.00002182',
            mean_motion_second_derivative='00000-0',
            radiation_pressure_coefficient='-11606-4',
            ephemeris_type='0',
            element_set_number='292',
            checksum='7',
            inclination='51.6416',
            right_ascension_of_descending_node='247.4627',
            eccentricity='0006703',
            argument_of_perigee='130.5360',
            mean_anomaly='325.0288',
            mean_motion='15.72125391',
            revolution_number_at_epoch='56353'
        )

    def given_a_rhodesmill_satellite_loaded_from_the_international_space_station_tle(self) -> None:
        tle_file = Path(get_script_directory(__file__), 'international_space_station_tle.tle')
        self._rhodesmill_satellite = loadSatellites(sat_tles=str(tle_file))[0]

    def when_the_cu_satellite_is_converted_into_rhodesmill(self) -> None:
        self._converted_satellite = self._cu_satellite.to_rhodesmill()

    def then_the_satellites_should_match(self) -> None:
        assert self._models_match() and self._non_model_properties_match()

    def _models_match(self) -> bool:
        for attribute in dir(self._converted_satellite.model):
            built_satellite_value = getattr(self._converted_satellite.model, attribute)
            should_test_attribute = not re.compile('^_').match(attribute) \
                                    and type(built_satellite_value) not in [types.BuiltinMethodType, types.MethodType]
            if should_test_attribute and built_satellite_value != getattr(self._rhodesmill_satellite.model, attribute):
                return False
        return True

    def _non_model_properties_match(self) -> bool:
        built_satellite_model = self._converted_satellite.model
        expected_satellite_model = self._rhodesmill_satellite.model
        self._converted_satellite.model = None
        self._rhodesmill_satellite.model = None

        is_match = pickle.dumps(self._converted_satellite) == pickle.dumps(self._rhodesmill_satellite)

        self._converted_satellite.model = built_satellite_model
        self._rhodesmill_satellite.model = expected_satellite_model

        return is_match
