from satellite_determination.dataclasses.coordinates import Coordinates
from satellite_determination.dataclasses.facility import Facility

ARBITRARY_FACILITY = Facility(
    beamwidth=3.,
    coordinates=Coordinates(latitude=1., longitude=2.),
    elevation=1.,
    name='name'
)
