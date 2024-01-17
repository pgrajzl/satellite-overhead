from sopp.custom_dataclasses.satellite.satellite import Satellite
from sopp.custom_dataclasses.satellite.mean_motion import MeanMotion
from sopp.custom_dataclasses.satellite.tle_information import TleInformation
from sopp.satellite_filters.filters import (
    name_contains_filter,
    name_does_not_contain_filter,
    name_is_filter,
    leo_filter,
    meo_filter,
    geo_filter,
)


class TestFilters:
    LEO_MEAN_MOTION = 0.00798
    MEO_MEAN_MOTION = 0.066
    GEO_MEAN_MOTION = 0.004375

    def test_name_contains_filter(self):
        expected = [self.sat0, self.sat1]
        actual = list(filter(name_contains_filter('TestSatellite'), self.satellites))
        assert actual == expected

    def test_name_does_not_contain_filter(self):
        expected = [self.sat2, self.sat3]
        actual = list(filter(name_does_not_contain_filter('TestSatellite'), self.satellites))
        assert actual == expected

    def test_name_is_filter(self):
        expected =  [self.sat2]
        actual = list(filter(name_is_filter('ISS'), self.satellites))
        assert actual == expected

    def test_leo_filter(self):
        expected = [self.sat1, self.sat2]
        actual = list(filter(leo_filter(), self.satellites))
        assert actual == expected

    def test_meo_filter(self):
        expected = [self.sat0]
        actual = list(filter(meo_filter(), self.satellites))
        assert actual == expected

    def test_geo_filter(self):
        expected = [self.sat3]
        actual = list(filter(geo_filter(), self.satellites))
        assert actual == expected

    @property
    def sat0(self):
        sat0 = Satellite(name='TestSatellite0')
        sat0.tle_information = self.arbitrary_tle_information
        sat0.tle_information.mean_motion = MeanMotion(0, 0, self.LEO_MEAN_MOTION)
        return sat0

    @property
    def sat1(self):
        sat1 = Satellite(name='TestSatellite1')
        sat1.tle_information = self.arbitrary_tle_information
        sat1.tle_information.mean_motion=MeanMotion(0, 0, self.MEO_MEAN_MOTION)
        return sat1


    @property
    def sat2(self):
        sat2 = Satellite(name='ISS')
        sat2.tle_information = self.arbitrary_tle_information
        sat2.tle_information.mean_motion=MeanMotion(0, 0, self.MEO_MEAN_MOTION)
        return sat2

    @property
    def sat3(self):
        sat3 =Satellite(name='Cosmos')
        sat3.tle_information = self.arbitrary_tle_information
        sat3.tle_information.mean_motion=MeanMotion(0, 0, self.GEO_MEAN_MOTION)
        return sat3

    @property
    def satellites(self):
        return [self.sat0, self.sat1, self.sat2, self.sat3]

    @property
    def arbitrary_tle_information(self):
        return TleInformation(
            argument_of_perigee=0.0,
            drag_coefficient=0.0,
            eccentricity=0.0,
            epoch_days=0.0,
            inclination=0.0,
            mean_anomaly=0.0,
            mean_motion=MeanMotion(0, 0, 0),
            revolution_number=0,
            right_ascension_of_ascending_node=0.0,
            satellite_number=0,
            classification='U',
            international_designator=None
        )
