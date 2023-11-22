from sopp.dataclasses.coordinates import Coordinates
from sopp.dataclasses.facility import Facility

ARBITRARY_FACILITY = Facility(
    beamwidth=3.,
    coordinates=Coordinates(latitude=1., longitude=2.),
    elevation=1.,
    name='name'
)
