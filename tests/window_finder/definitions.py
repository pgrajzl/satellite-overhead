from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility

ARBITRARY_FACILITY = Facility(
    elevation=1.,
    coordinates=Coordinates(latitude=1., longitude=2.),
    beamwidth=3.,
    name='name',
    azimuth=30
)
