from datetime import datetime

import pytz
from skyfield.api import load

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.satellite.international_designator import InternationalDesignator
from satellite_determination.custom_dataclasses.satellite.mean_motion import MeanMotion
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.satellite.tle_information import TleInformation
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellite_position_with_respect_to_facility_retriever.satellite_position_with_respect_to_facility_retriever_rhodesmill import \
    SatellitePositionWithRespectToFacilityRetrieverRhodesmill


class TestSatellitePositionWithRespectToFacilityRetrieverRhodesmill:
    def test_altitude_can_be_negative(self):
        timestamp = datetime(year=2023, month=6, day=7, tzinfo=pytz.UTC)
        facility = Facility(Coordinates(latitude=0, longitude=0))
        retriever = SatellitePositionWithRespectToFacilityRetrieverRhodesmill(satellite=self._arbitrary_satellite,
                                                                              timestamp=timestamp,
                                                                              facility=facility)
        position = retriever.run()
        assert position == PositionTime(altitude=-15.275020193822348,
                                        azimuth=301.7439304748296,
                                        time=timestamp)

    def test_azimuth_can_be_greater_than_180(self):
        timestamp = datetime(year=2023, month=6, day=7, tzinfo=pytz.UTC)
        facility = Facility(Coordinates(latitude=0, longitude=0))
        retriever = SatellitePositionWithRespectToFacilityRetrieverRhodesmill(satellite=self._arbitrary_satellite,
                                                                              timestamp=timestamp,
                                                                              facility=facility)
        position = retriever.run()
        assert position == PositionTime(altitude=-15.275020193822348,
                                        azimuth=301.7439304748296,
                                        time=timestamp)

    @property
    def _arbitrary_satellite(self) -> Satellite:
        """
        From 0 COSMOS 1932 DEB
        """
        return Satellite(
                name='ARBITRARY SATELLITE',
                tle_information=TleInformation(
                    argument_of_perigee=5.153187590939126,
                    drag_coefficient=0.00015211,
                    eccentricity=0.0057116,
                    epoch_days=26633.28893622,
                    inclination=1.1352005427406557,
                    international_designator=InternationalDesignator(
                        year=88,
                        launch_number=19,
                        launch_piece='F'
                    ),
                    mean_anomaly=4.188343400497881,
                    mean_motion=MeanMotion(
                        first_derivative=2.363466695408988e-12,
                        second_derivative=0.0,
                        value=0.060298700041442894
                    ),
                    revolution_number=95238,
                    right_ascension_of_ascending_node=2.907844197528697,
                    satellite_number=28275,
                    classification='U'
                ),
                frequency=[]
            )
