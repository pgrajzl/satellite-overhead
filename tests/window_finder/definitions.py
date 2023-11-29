from sopp.custom_dataclasses.coordinates import Coordinates
from sopp.custom_dataclasses.facility import Facility

ARBITRARY_FACILITY = Facility(
    beamwidth=3.,
    coordinates=Coordinates(latitude=1., longitude=2.),
    elevation=1.,
    name='name'
)
