import pytz
from datetime import datetime, timedelta

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.position import Position
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
            position=Position(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                              azimuth=ARBITRARY_SATELLITE_AZIMUTH),
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
                                             antenna_direction_path=[PositionTime(position=Position(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                                                                                                    azimuth=ARBITRARY_SATELLITE_AZIMUTH),
                                                                                  time=arbitrary_datetime)],
                                             satellite_position_with_respect_to_facility_retriever_class=SatellitePositionWithRespectToFacilityRetrieverStub)
        windows = event_finder.get_satellites_crossing_main_beam()

        assert len(windows) == 1

        assert windows[0].satellite == arbitrary_satellite
        assert windows[0].overhead_time.begin == arbitrary_time_window.begin
        assert windows[0].overhead_time.end == arbitrary_time_window.end - timedelta(seconds=1)

    def test_multiple_satellites(self):
        arbitrary_satellites = [Satellite(name='arbitrary'), Satellite(name='arbitrary2')]
        arbitrary_datetime = datetime.now(tz=pytz.utc)
        arbitrary_time_window = TimeWindow(begin=arbitrary_datetime,
                                           end=arbitrary_datetime + timedelta(seconds=2))
        arbitrary_reservation = Reservation(facility=Facility(coordinates=Coordinates(latitude=0, longitude=0)),
                                            time=arbitrary_time_window)
        event_finder = EventFinderRhodesMill(list_of_satellites=arbitrary_satellites,
                                             reservation=arbitrary_reservation,
                                             antenna_direction_path=[PositionTime(position=Position(altitude=ARBITRARY_SATELLITE_ALTITUDE,
                                                                                                    azimuth=ARBITRARY_SATELLITE_AZIMUTH),
                                                                                  time=arbitrary_datetime)],
                                             satellite_position_with_respect_to_facility_retriever_class=SatellitePositionWithRespectToFacilityRetrieverStub)
        windows = event_finder.get_satellites_crossing_main_beam()

        assert len(windows) == 2

        assert windows[0].satellite == arbitrary_satellites[0]
        assert windows[0].overhead_time.begin == arbitrary_time_window.begin
        assert windows[0].overhead_time.end == arbitrary_time_window.end - timedelta(seconds=1)

        assert windows[1].satellite == arbitrary_satellites[1]
        assert windows[1].overhead_time.begin == arbitrary_time_window.begin
        assert windows[1].overhead_time.end == arbitrary_time_window.end - timedelta(seconds=1)

    def test_multiple_antenna_positions_with_azimuth_filtering(self):
        arbitrary_satellite = Satellite(name='arbitrary')
        arbitrary_datetime = datetime.now(tz=pytz.utc)

        arbitrary_time_window = TimeWindow(
            begin=arbitrary_datetime,
            end=arbitrary_datetime + timedelta(seconds=5)
        )

        arbitrary_reservation = Reservation(
            facility=Facility(coordinates=Coordinates(latitude=0, longitude=0)),
            time=arbitrary_time_window
        )

        altitude_outside_beamwidth = ARBITRARY_SATELLITE_ALTITUDE + arbitrary_reservation.facility.half_beamwidth + SMALL_EPSILON
        event_finder = EventFinderRhodesMill(
            list_of_satellites=[arbitrary_satellite],
            reservation=arbitrary_reservation,
            antenna_direction_path=[
                PositionTime(
                    position=Position(altitude=ARBITRARY_SATELLITE_ALTITUDE, azimuth=ARBITRARY_SATELLITE_AZIMUTH),
                    time=arbitrary_datetime
                ),
                PositionTime(
                    position=Position(altitude=altitude_outside_beamwidth, azimuth=ARBITRARY_SATELLITE_AZIMUTH),
                    time=arbitrary_datetime + timedelta(seconds=1)
                ),
                PositionTime(
                    position=Position(altitude=ARBITRARY_SATELLITE_ALTITUDE, azimuth=ARBITRARY_SATELLITE_AZIMUTH),
                    time=arbitrary_datetime + timedelta(seconds=2)
                ),
                PositionTime(
                    position=Position(altitude=ARBITRARY_SATELLITE_ALTITUDE, azimuth=ARBITRARY_SATELLITE_AZIMUTH),
                    time=arbitrary_datetime + timedelta(seconds=3)
                ),
                PositionTime(
                    position=Position(altitude=ARBITRARY_SATELLITE_ALTITUDE, azimuth=ARBITRARY_SATELLITE_AZIMUTH),
                    time=arbitrary_datetime + timedelta(seconds=4)
                )
            ],
            satellite_position_with_respect_to_facility_retriever_class=SatellitePositionWithRespectToFacilityRetrieverStub
        )

        windows = event_finder.get_satellites_crossing_main_beam()

        assert len(windows) == 2

        assert windows[0].satellite == arbitrary_satellite
        assert windows[0].overhead_time.begin == arbitrary_datetime
        assert windows[0].overhead_time.end == arbitrary_datetime

        assert windows[1].satellite == arbitrary_satellite
        assert windows[1].overhead_time.begin == arbitrary_datetime + timedelta(seconds=2)
        assert windows[1].overhead_time.end == arbitrary_datetime + timedelta(seconds=4)
