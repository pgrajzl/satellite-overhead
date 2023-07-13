from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite
from skyfield.toposlib import wgs84

from satellite_determination.custom_dataclasses.position import Position
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellite_position_with_respect_to_facility_retriever.satellite_position_with_respect_to_facility_retriever import \
    SatellitePositionWithRespectToFacilityRetriever


RHODESMILL_TIMESCALE = load.timescale()


class SatellitePositionWithRespectToFacilityRetrieverRhodesmill(SatellitePositionWithRespectToFacilityRetriever):
    _satellite_rhodesmill_cache = {}

    def run(self) -> PositionTime:
        satellite_rhodesmill_with_respect_to_facility = self._satellite_rhodesmill - wgs84.latlon(
            latitude_degrees=self._facility.coordinates.latitude,
            longitude_degrees=self._facility.coordinates.longitude,
            elevation_m=self._facility.elevation)

        timestamps_rhodesmill = RHODESMILL_TIMESCALE.from_datetime(self._timestamp)
        topocentric = satellite_rhodesmill_with_respect_to_facility.at(timestamps_rhodesmill)
        altitude, azimuth, _ = topocentric.altaz()
        return PositionTime(
            position=Position(altitude=altitude.degrees, azimuth=azimuth.degrees),
            time=self._timestamp
        )

    @property
    def _satellite_rhodesmill(self) -> EarthSatellite:
        if self._satellite.name not in self._satellite_rhodesmill_cache:
            self._satellite_rhodesmill_cache[self._satellite.name] = self._satellite.to_rhodesmill()
        return self._satellite_rhodesmill_cache[self._satellite.name]
