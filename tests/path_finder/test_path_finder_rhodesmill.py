import pytest

from satellite_determination.dataclasses.observation_target import ObservationTarget
from satellite_determination.path_finder.observation_path_finder_rhodesmill import ObservationPathFinderRhodesMill
from path_finder_base_test import PathFinderBaseTest


class TestPathFinderRhodesMill(PathFinderBaseTest):
    PathFinderClass = ObservationPathFinderRhodesMill

    @pytest.mark.parametrize('declination, right_ascension, expected', [
        ('12d15m18s', '12h15m18s', (12, 15, 18)),
        ('12d15m18.5s', '12h15m18.5s', (12, 15, 18.5)),
        ('-38d6m50.8s', '-38h6m50.8s', (-38, 6, 50.8)),
    ])
    def test_ra_dec_to_rhodesmill(self, declination, right_ascension, expected):
        obs_target = ObservationTarget(declination=declination, right_ascension=right_ascension)
        actual_ra = ObservationPathFinderRhodesMill.right_ascension_to_rhodesmill(obs_target)
        actual_dec = ObservationPathFinderRhodesMill.declination_to_rhodesmill(obs_target)

        assert actual_ra == expected
        assert actual_dec == expected
