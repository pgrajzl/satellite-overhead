import pytest

from sopp.utilities import read_datetime_string_as_utc
from sopp.custom_dataclasses.facility import Facility
from sopp.custom_dataclasses.coordinates import Coordinates
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.custom_dataclasses.observation_target import ObservationTarget
from sopp.path_finder.observation_path_finder_rhodesmill import ObservationPathFinderRhodesmill
from sopp.path_finder.observation_path_finder_astropy import ObservationPathFinderAstropy


class TestPathFinderEquivalency:
    @pytest.mark.parametrize('declination, right_ascension', [
        ('7d24m26s', '5h55m10s'),
        ('-38d6m50.8s', '4h42m'),
    ])
    def test_equivalency(self, declination, right_ascension):
        facility = facility = Facility(
            Coordinates(
                latitude=0.0,
                longitude=0.0,
            ),
            elevation=0,
            name='Null Island',
        )

        time_window = TimeWindow(
            begin=read_datetime_string_as_utc('2023-09-23T05:49:00.000000'),
            end=read_datetime_string_as_utc('2023-09-23T06:56:00.000000'),
        )

        obs_target = ObservationTarget(declination=declination, right_ascension=right_ascension)

        astro = ObservationPathFinderAstropy(facility, obs_target, time_window).calculate_path()
        rhodes = ObservationPathFinderRhodesmill(facility, obs_target, time_window).calculate_path()

        self._assert_alt_eq(astro, rhodes)
        self._assert_az_eq(astro, rhodes)

    def _assert_alt_eq(self, astro, rhodes, tolerance=0.001):
        assert all(abs(a.position.altitude - r.position.altitude) <= tolerance for a, r in zip(astro, rhodes))

    def _assert_az_eq(self, astro, rhodes, tolerance=0.0015):
        assert all(abs(a.position.azimuth - r.position.azimuth) <= tolerance for a, r in zip(astro, rhodes))
