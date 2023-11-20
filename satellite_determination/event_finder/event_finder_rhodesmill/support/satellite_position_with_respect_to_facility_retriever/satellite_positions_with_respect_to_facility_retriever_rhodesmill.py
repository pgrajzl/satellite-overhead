from datetime import datetime
from typing import List

from skyfield.api import load
from skyfield.toposlib import wgs84

from satellite_determination.event_finder.event_finder_rhodesmill.support.satellite_position_with_respect_to_facility_retriever.satellite_positions_with_respect_to_facility_retriever import \
    SatellitePositionsWithRespectToFacilityRetriever
from satellite_determination.custom_dataclasses.position import Position
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite


RHODESMILL_TIMESCALE = load.timescale()


class SatellitePositionsWithRespectToFacilityRetrieverRhodesmill(SatellitePositionsWithRespectToFacilityRetriever):
    def __init__(self, facility: Facility, datetimes: List[datetime]):
        super().__init__(facility, datetimes)
        self._timescales = RHODESMILL_TIMESCALE.from_datetimes(datetimes)
        self._facility_latlon = self._calculate_facility_latlon(self._facility)

    def run(self, satellite: Satellite) -> List[PositionTime]:
        satellite_rhodesmill_with_respect_to_facility = satellite.to_rhodesmill() - self._facility_latlon

        topocentric = satellite_rhodesmill_with_respect_to_facility.at(self._timescales)
        altitude, azimuth, _ = topocentric.altaz()

        return [
            PositionTime(
                Position(altitude=altitude, azimuth=azimuth),
                time=time
            )
            for altitude, azimuth, time in zip(altitude.degrees, azimuth.degrees, self._datetimes)
        ]

    def _calculate_facility_latlon(self, facility: Facility):
        return wgs84.latlon(
            latitude_degrees=facility.coordinates.latitude,
            longitude_degrees=facility.coordinates.longitude,
            elevation_m=facility.elevation
        )
