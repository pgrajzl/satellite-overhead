import pytz
from datetime import datetime, timedelta

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesMill
from satellite_determination.event_finder.event_finder_rhodesmill.support.satellite_position_with_respect_to_facility_retriever.satellite_position_with_respect_to_facility_retriever import \
    SatellitePositionWithRespectToFacilityRetriever
from tests.definitions import SMALL_EPSILON

ARBITRARY_SATELLITE_ALTITUDE = 0
ARBITRARY_SATELLITE_AZIMUTH = 0


class SatellitePositionWithRespectToFacilityRetrieverStub(SatellitePositionWithRespectToFacilityRetriever):
    def run(self) -> PositionTime:
        return PositionTime(
            altitude=ARBITRARY_SATELLITE_ALTITUDE,
            azimuth=ARBITRARY_SATELLITE_AZIMUTH,
            time=self._timestamp
        )


class TestEventFinderRhodesmill:
    def test_single_satellite(self):
        arbitrary_satellite = Satellite(name='arbitrary')
        arbitrary_datetime = datetime.now(tz=pytz.utc)
        arbitrary_time_window = TimeWindow(begin=arbitrary_datetime,
                                           end=arbitrary_datetime + timedelta(seconds=2))
        arbitrary_reservation = Reservation(facility=Facility(coordinates=Coordinates(latitude=0, longitude=0)),
                                            time=arbitrary_time_window)
        event_finder = EventFinderRhodesMill(list_of_satellites=[arbitrary_satellite],
                                             reservation=arbitrary_reservation,
                                             antenna_direction_path=[PositionTime(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                                                                                  azimuth=ARBITRARY_SATELLITE_AZIMUTH,
                                                                                  time=arbitrary_datetime)],
                                             satellite_position_with_respect_to_facility_retriever_class=SatellitePositionWithRespectToFacilityRetrieverStub)
        windows = event_finder.get_satellites_crossing_main_beam()
        assert windows == [OverheadWindow(satellite=arbitrary_satellite, overhead_time=arbitrary_time_window)]

    def test_multiple_satellites(self):
        arbitrary_satellites = [Satellite(name='arbitrary'), Satellite(name='arbitrary2')]
        arbitrary_datetime = datetime.now(tz=pytz.utc)
        arbitrary_time_window = TimeWindow(begin=arbitrary_datetime,
                                           end=arbitrary_datetime + timedelta(seconds=2))
        arbitrary_reservation = Reservation(facility=Facility(coordinates=Coordinates(latitude=0, longitude=0)),
                                            time=arbitrary_time_window)
        event_finder = EventFinderRhodesMill(list_of_satellites=arbitrary_satellites,
                                             reservation=arbitrary_reservation,
                                             antenna_direction_path=[PositionTime(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                                                                                  azimuth=ARBITRARY_SATELLITE_AZIMUTH,
                                                                                  time=arbitrary_datetime)],
                                             satellite_position_with_respect_to_facility_retriever_class=SatellitePositionWithRespectToFacilityRetrieverStub)
        windows = event_finder.get_satellites_crossing_main_beam()
        assert windows == [OverheadWindow(satellite=satellite, overhead_time=arbitrary_time_window)
                           for satellite in arbitrary_satellites]

    def test_multiple_antenna_positions_with_azimuth_filtering(self):
        arbitrary_satellite = Satellite(name='arbitrary')
        arbitrary_datetime = datetime.now(tz=pytz.utc)
        arbitrary_time_window = TimeWindow(begin=arbitrary_datetime,
                                           end=arbitrary_datetime + timedelta(seconds=3))
        arbitrary_reservation = Reservation(facility=Facility(coordinates=Coordinates(latitude=0, longitude=0)),
                                            time=arbitrary_time_window)
        altitude_outside_beamwidth = ARBITRARY_SATELLITE_ALTITUDE + arbitrary_reservation.facility.half_beamwidth + SMALL_EPSILON
        event_finder = EventFinderRhodesMill(list_of_satellites=[arbitrary_satellite],
                                             reservation=arbitrary_reservation,
                                             antenna_direction_path=[
                                                 PositionTime(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                                                              azimuth=ARBITRARY_SATELLITE_AZIMUTH,
                                                              time=arbitrary_datetime),
                                                 PositionTime(altitude=altitude_outside_beamwidth,
                                                              azimuth=ARBITRARY_SATELLITE_AZIMUTH,
                                                              time=arbitrary_datetime + timedelta(seconds=1)),
                                                 PositionTime(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                                                              azimuth=ARBITRARY_SATELLITE_AZIMUTH,
                                                              time=arbitrary_datetime + timedelta(seconds=2))
                                             ],
                                             satellite_position_with_respect_to_facility_retriever_class=SatellitePositionWithRespectToFacilityRetrieverStub)
        windows = event_finder.get_satellites_crossing_main_beam()
        assert windows == [
            OverheadWindow(satellite=arbitrary_satellite, overhead_time=TimeWindow(begin=arbitrary_datetime,
                                                                                   end=arbitrary_datetime + timedelta(seconds=1))),
            OverheadWindow(satellite=arbitrary_satellite, overhead_time=TimeWindow(begin=arbitrary_datetime + timedelta(seconds=2),
                                                                                   end=arbitrary_datetime + timedelta(seconds=3)))
        ]