import pickle
import re
import types
from pathlib import Path

from satellite_determination.ListOfSatellites import loadSatellites
from satellite_determination.custom_dataclasses.satellite.international_designator import InternationalDesignator
from satellite_determination.custom_dataclasses.satellite.mean_motion import MeanMotion
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.satellite.tle_information import TleInformation
from tests.utilities import get_script_directory


class TestSatelliteToRhodesMill:
    def test_satellite_can_translate_to_rhodesmill(self):
        self.given_a_cu_satellite_with_international_space_station_properties()
        self.given_a_rhodesmill_satellite_loaded_from_the_international_space_station_tle()
        self.when_the_cu_satellite_is_converted_into_rhodesmill()
        self.then_the_satellites_should_match()

    def given_a_cu_satellite_with_international_space_station_properties(self) -> None:
        self._cu_satellite = Satellite(
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
            ),
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
