from datetime import datetime, timezone
from functools import cached_property

from skyfield.api import load, wgs84
from skyfield.timelib import Time, Timescale

from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.satellite.international_designator import InternationalDesignator
from satellite_determination.custom_dataclasses.satellite.mean_motion import MeanMotion
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.satellite.tle_information import TleInformation


class TestRhodesmillIntegration:
    def test_events_found_on_window_that_encompasses_full_satellite_pass(self):
        time_begin = self._datetime_to_rhodesmill_time(minute=0)
        time_end = self._datetime_to_rhodesmill_time(minute=59)
        coordinates = wgs84.latlon(40.8178049, -121.4695413)
        rhodesmill_earthsat = self._satellite.to_rhodesmill()
        event_times, events = rhodesmill_earthsat.find_events(topos=coordinates,
                                                              t0=time_begin,
                                                              t1=time_end,
                                                              altitude_degrees=0)
        assert len(events)


    def _datetime_to_rhodesmill_time(self, minute: int) -> Time:
        return self._rhodesmill_timescale.from_datetime(datetime(2023, 3, 30, 12, minute, tzinfo=timezone.utc))

    @cached_property
    def _rhodesmill_timescale(self) -> Timescale:
        return load.timescale()

    @property
    def _satellite(self) -> Satellite:
        return Satellite(name='SAUDISAT 2',
                         tle_information=TleInformation(argument_of_perigee=2.6581678667138995,
                                                        drag_coefficient=8.4378e-05,
                                                        eccentricity=0.0025973,
                                                        epoch_days=26801.46955532,
                                                        inclination=1.7179345640550268,
                                                        international_designator=InternationalDesignator(year=4,
                                                                                                         launch_number=25,
                                                                                                         launch_piece='F'),
                                                        mean_anomaly=3.6295308619113436,
                                                        mean_motion=MeanMotion(first_derivative=9.605371056982682e-12,
                                                                               second_derivative=0.0,
                                                                               value=0.06348248105551128),
                                                        revolution_number=200,
                                                        right_ascension_of_ascending_node=1.7778098293739442,
                                                        satellite_number=28371,
                                                        classification='U'),
                         frequency=[FrequencyRange(frequency=137.513, bandwidth=None, status='active')])
