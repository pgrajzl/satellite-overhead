from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility

ARBITRARY_FACILITY = Facility(
    altitude=1.,
    point_coordinates=Coordinates(latitude=1., longitude=2.),
    name='name',
    azimuth=30
)
