from datetime import datetime, timedelta

import pytz

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.position import Position
from satellite_determination.custom_dataclasses.position_time import PositionTime
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesMill
from tests.definitions import SMALL_EPSILON
from tests.event_finder.event_finder_rhodesmill.test_event_finder_rhodesmill import ARBITRARY_SATELLITE_ALTITUDE, \
    ARBITRARY_SATELLITE_AZIMUTH, SatellitePositionWithRespectToFacilityRetrieverStub


class TestEventFinderReservationStartTime:
    def test_reservation_begins_part_way_through_antenna_position_time(self):
        arbitrary_satellite = Satellite(name='arbitrary')
        arbitrary_datetime = datetime.now(tz=pytz.utc)
        arbitrary_time_window = TimeWindow(begin=arbitrary_datetime,
                                           end=arbitrary_datetime + timedelta(seconds=2))
        arbitrary_reservation = Reservation(facility=Facility(coordinates=Coordinates(latitude=0, longitude=0)),
                                            time=arbitrary_time_window)
        event_finder = EventFinderRhodesMill(list_of_satellites=[arbitrary_satellite],
                                             reservation=arbitrary_reservation,
                                             antenna_direction_path=[PositionTime(position=Position(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                                                                                                    azimuth=ARBITRARY_SATELLITE_AZIMUTH),
                                                                                  time=arbitrary_datetime - timedelta(seconds=1))],
                                             satellite_position_with_respect_to_facility_retriever_class=SatellitePositionWithRespectToFacilityRetrieverStub)
        windows = event_finder.get_satellites_crossing_main_beam()
        assert windows == [OverheadWindow(satellite=arbitrary_satellite, overhead_time=arbitrary_time_window)]

    def test_antenna_positions_that_end_before_reservation_starts_are_not_included(self):
        arbitrary_satellite = Satellite(name='arbitrary')
        arbitrary_datetime = datetime.now(tz=pytz.utc)
        arbitrary_time_window = TimeWindow(begin=arbitrary_datetime,
                                           end=arbitrary_datetime + timedelta(seconds=2))
        arbitrary_reservation = Reservation(facility=Facility(coordinates=Coordinates(latitude=0, longitude=0)),
                                            time=arbitrary_time_window)
        altitude_inside_beam_width = ARBITRARY_SATELLITE_ALTITUDE
        altitude_outside_beam_width = ARBITRARY_SATELLITE_ALTITUDE + arbitrary_reservation.facility.half_beamwidth + SMALL_EPSILON
        arbitrary_time_before_reservation_starts = arbitrary_datetime - timedelta(seconds=1)
        antenna_position_that_ends_before_reservation_begins = PositionTime(position=Position(altitude=altitude_inside_beam_width,
                                                                                              azimuth=ARBITRARY_SATELLITE_AZIMUTH),
                                                                            time=arbitrary_time_before_reservation_starts - timedelta(seconds=1))
        antenna_position_that_has_no_satellites_in_beam = PositionTime(position=Position(altitude=altitude_outside_beam_width,
                                                                                         azimuth=ARBITRARY_SATELLITE_AZIMUTH),
                                                                       time=arbitrary_time_before_reservation_starts)
        event_finder = EventFinderRhodesMill(list_of_satellites=[arbitrary_satellite],
                                             reservation=arbitrary_reservation,
                                             antenna_direction_path=[
                                                 antenna_position_that_ends_before_reservation_begins,
                                                 antenna_position_that_has_no_satellites_in_beam],
                                             satellite_position_with_respect_to_facility_retriever_class=SatellitePositionWithRespectToFacilityRetrieverStub)
        windows = event_finder.get_satellites_crossing_main_beam()
        assert windows == []
