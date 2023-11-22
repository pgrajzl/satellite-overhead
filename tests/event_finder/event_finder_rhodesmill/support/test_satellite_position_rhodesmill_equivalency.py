from sopp.event_finder.event_finder_rhodesmill.support.evenly_spaced_time_intervals_calculator import \
    EvenlySpacedTimeIntervalsCalculator
from sopp.event_finder.event_finder_rhodesmill.support.satellite_position_with_respect_to_facility_retriever.satellite_positions_with_respect_to_facility_retriever_rhodesmill import \
    SatellitePositionsWithRespectToFacilityRetrieverRhodesmill
from sopp.event_finder.event_finder_rhodesmill.support.satellite_position_with_respect_to_facility_retriever.satellite_position_with_respect_to_facility_retriever_rhodesmill import \
    SatellitePositionWithRespectToFacilityRetrieverRhodesmill
from sopp.dataclasses.facility import Facility
from sopp.dataclasses.coordinates import Coordinates
from sopp.dataclasses.time_window import TimeWindow
from sopp.dataclasses.satellite.international_designator import InternationalDesignator
from sopp.dataclasses.satellite.mean_motion import MeanMotion
from sopp.dataclasses.satellite.satellite import Satellite
from sopp.dataclasses.satellite.tle_information import TleInformation
from sopp.utilities import read_datetime_string_as_utc

from datetime import timedelta
from functools import cached_property


class TestSatellitePositionWithRespectToFacilityRetrieverEquivalency:
    def test_equivalency(self):
        multi = SatellitePositionsWithRespectToFacilityRetrieverRhodesmill(
            facility=self._facility,
            datetimes=self._times,
        )
        actual = multi.run(satellite=self._satellite)
        expected = [
            SatellitePositionWithRespectToFacilityRetrieverRhodesmill(
                satellite=self._satellite,
                timestamp=time,
                facility=self._facility
            ).run()
            for time in self._times
        ]

        assert (all(abs(s.position.altitude - o.position.altitude) <= .00001) for s, o in zip(actual, expected))
        assert (all(abs(s.position.azimuth - o.position.azimuth) <= .00001) for s, o in zip(actual, expected))

    @cached_property
    def _satellite(self) -> Satellite:
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

    @cached_property
    def _facility(self):
        facility = Facility(
            Coordinates(
                latitude=40.8178049,
                longitude=-121.4695413,
            ),
            elevation=986,
            name='HCRO',
        )

        return facility

    @cached_property
    def _times(self):
        time_window = TimeWindow(
            begin=read_datetime_string_as_utc('2023-10-06T00:00:00.000000'),
            end=read_datetime_string_as_utc('2023-10-06T0:10:00.000000'),
        )

        times = EvenlySpacedTimeIntervalsCalculator(
            time_window=time_window,
            resolution=timedelta(seconds=1)
        ).run()

        return times
