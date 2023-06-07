from functools import cached_property

from skyfield.api import load
from skyfield.timelib import Timescale
from skyfield.toposlib import wgs84

from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellite_position_with_respect_to_facility_retriever.satellite_position_with_respect_to_facility_retriever import \
    SatellitePositionWithRespectToFacilityRetriever


class SatellitePositionWithRespectToFacilityRetrieverRhodesmill(SatellitePositionWithRespectToFacilityRetriever):
    def run(self) -> PositionTime:
        satellite_rhodesmill = self._satellite.to_rhodesmill()
        satellite_rhodesmill_with_respect_to_facility = satellite_rhodesmill - wgs84.latlon(
            latitude_degrees=self._facility.coordinates.latitude,
            longitude_degrees=self._facility.coordinates.longitude,
            elevation_m=self._facility.elevation)

        timestamps_rhodesmill = self._rhodesmill_timescale.from_datetime(self._timestamp)
        topocentric = satellite_rhodesmill_with_respect_to_facility.at(timestamps_rhodesmill)
        altitude, azimuth, _ = topocentric.altaz()
        return PositionTime(
            altitude=altitude.degrees,
            azimuth=azimuth.degrees,
            time=self._timestamp
        )

    @cached_property
    def _rhodesmill_timescale(self) -> Timescale:
        return load.timescale()
