from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import List

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.time_window import TimeWindow


class EventTypesRhodesmill(Enum):
    ENTERS = 0 #Skyfield API returns events as 0, 1, or 2 for enters, culminates, exits
    CULMINATES = 1
    EXITS = 2 #ASK NICK WHY AUTO()


@dataclass
class EventRhodesmill:
    event_type: EventTypesRhodesmill
    satellite: Satellite
    timestamp: datetime


class OverheadWindowFromEvents:
    def __init__(self, events: List[EventRhodesmill], reservation: Reservation):
        self._events = events
        self._reservation = reservation

    def get(self) -> List[OverheadWindow]:
        enter_events, culminate_events, exit_events = ([event for event in self._events if event.event_type == event_type]
                                     for event_type in EventTypesRhodesmill)
        if (len(self._events) == 1) and (self._events[0].event_type == EventTypesRhodesmill.CULMINATES): #handles sat that is in view for entire reservation
            time_window = TimeWindow(begin=self._reservation.time.begin, end=self._reservation.time.end)
            overhead_windows = [OverheadWindow(satellite=self._events[0].satellite, overhead_time=time_window)]
        else:
            if len(enter_events) != len(exit_events): #Handle case where a satellite starts or ends in observation area
                if self._events[0].event_type == EventTypesRhodesmill.ENTERS: #the first event is the satellite entering view, so it didn't start in observation area
                    end_reservation_event = EventRhodesmill(event_type=EventTypesRhodesmill.EXITS, satellite=self._events[0].satellite, timestamp=self._reservation.time.end)
                    exit_events.append(end_reservation_event)
                elif self._events[0].event_type == EventTypesRhodesmill.EXITS: #the first event is an exit, so the sat starts in view
                    start_reservation_event = EventRhodesmill(event_type=EventTypesRhodesmill.ENTERS, satellite=self._events[0].satellite, timestamp=self._reservation.time.begin)
                    enter_events.insert(0, start_reservation_event)
            enter_and_exit_pairs = zip(enter_events, exit_events)
            time_windows = [TimeWindow(begin=begin_event.timestamp, end=exit_event.timestamp) for begin_event, exit_event in enter_and_exit_pairs]
            overhead_windows = [OverheadWindow(satellite=self._events[0].satellite, overhead_time=time_window) for time_window in time_windows]
        return overhead_windows


class TestOverheadWindowFromEvents:

    def test_one_satellite_only_leaves(self):
        event = EventRhodesmill(
            event_type=EventTypesRhodesmill.EXITS,
            satellite=self._arbitrary_satellite,
            timestamp=self._arbitrary_date
        )
        overhead_windows = OverheadWindowFromEvents(events=[event], reservation=self._arbitrary_reservation_with_nonzero_timewindow).get()
        assert overhead_windows == [
            OverheadWindow(
                satellite=self._arbitrary_satellite,
                overhead_time=TimeWindow(
                    begin=self._arbitrary_reservation_with_nonzero_timewindow.time.begin,
                    end=event.timestamp
                )
            )
        ]

    def test_one_satellite_only_enters(self):
        event = EventRhodesmill(
            event_type=EventTypesRhodesmill.ENTERS,
            satellite=self._arbitrary_satellite,
            timestamp=self._arbitrary_date
        )
        overhead_windows = OverheadWindowFromEvents(events=[event], reservation=self._arbitrary_reservation_with_nonzero_timewindow).get()
        assert overhead_windows == [
            OverheadWindow(
                satellite=self._arbitrary_satellite,
                overhead_time=TimeWindow(
                    begin=event.timestamp,
                    end=self._arbitrary_reservation_with_nonzero_timewindow.time.end
                )
            )
        ]

    def test_one_satellite_stays_in_view(self):
        events = [
            EventRhodesmill(
                event_type=EventTypesRhodesmill.CULMINATES,
                satellite=self._arbitrary_satellite,
                timestamp=self._arbitrary_date)
        ]
        overhead_windows = OverheadWindowFromEvents(events=events, reservation=self._arbitrary_reservation_with_nonzero_timewindow).get()
        assert overhead_windows == [
            OverheadWindow(
                satellite=self._arbitrary_satellite,
                overhead_time=TimeWindow(
                    begin=self._arbitrary_reservation_with_nonzero_timewindow.time.begin,
                    end=self._arbitrary_reservation_with_nonzero_timewindow.time.end
                )
            )
        ]

    def test_one_satellite_enters_and_leaves(self):
        events = {
            EventTypesRhodesmill.ENTERS: EventRhodesmill(
                event_type=EventTypesRhodesmill.ENTERS,
                satellite=self._arbitrary_satellite,
                timestamp=self._arbitrary_date
            ),
            EventTypesRhodesmill.EXITS: EventRhodesmill(
                event_type=EventTypesRhodesmill.EXITS,
                satellite=self._arbitrary_satellite,
                timestamp=self._arbitrary_date + timedelta(hours=1)
            ),
        }
        overhead_windows = OverheadWindowFromEvents(events=list(events.values()), reservation=self._arbitrary_reservation_with_nonzero_timewindow).get()
        assert overhead_windows == [
            OverheadWindow(
                satellite=self._arbitrary_satellite,
                overhead_time=TimeWindow(
                    begin=events[EventTypesRhodesmill.ENTERS].timestamp,
                    end=events[EventTypesRhodesmill.EXITS].timestamp
                )
            )
        ]

    def test_one_satellite_enters_and_leaves_twice(self):
        events = [
            EventRhodesmill(
                event_type=EventTypesRhodesmill.ENTERS,
                satellite=self._arbitrary_satellite,
                timestamp=self._arbitrary_date
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.EXITS,
                satellite=self._arbitrary_satellite,
                timestamp=self._arbitrary_date + timedelta(hours=1)
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.ENTERS,
                satellite=self._arbitrary_satellite,
                timestamp=self._arbitrary_date_two
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.EXITS,
                satellite=self._arbitrary_satellite,
                timestamp=self._arbitrary_date_two + timedelta(hours=1)
            ),
        ]
        overhead_windows = OverheadWindowFromEvents(events=events, reservation=self._arbitrary_reservation_with_nonzero_timewindow).get()
        assert overhead_windows == [
            OverheadWindow(
                satellite=self._arbitrary_satellite,
                overhead_time=TimeWindow(
                    begin=events[0].timestamp,
                    end=events[1].timestamp
                )
            ),
            OverheadWindow(
                satellite=self._arbitrary_satellite,
                overhead_time=TimeWindow(
                    begin=events[2].timestamp,
                    end=events[3].timestamp
                )
            )
        ]

    def test_one_satellite_enters_leaves_enters(self):
        events = [
            EventRhodesmill(
                event_type=EventTypesRhodesmill.ENTERS,
                satellite=self._arbitrary_satellite,
                timestamp=self._arbitrary_date
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.EXITS,
                satellite=self._arbitrary_satellite,
                timestamp=self._arbitrary_date + timedelta(hours=1)
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.ENTERS,
                satellite=self._arbitrary_satellite,
                timestamp=self._arbitrary_date_two
            ),
        ]
        overhead_windows = OverheadWindowFromEvents(events=events, reservation=self._arbitrary_reservation_with_nonzero_timewindow).get()
        assert overhead_windows == [
            OverheadWindow(
                satellite=self._arbitrary_satellite,
                overhead_time=TimeWindow(
                    begin=events[0].timestamp,
                    end=events[1].timestamp
                )
            ),
            OverheadWindow(
                satellite=self._arbitrary_satellite,
                overhead_time=TimeWindow(
                    begin=events[2].timestamp,
                    end=self._arbitrary_reservation_with_nonzero_timewindow.time.end
                )
            )
        ]

    @property
    def _arbitrary_satellite(self) -> Satellite:
        return Satellite(name='name')

    @property
    def _arbitrary_date(self) -> datetime:
        return datetime(year=2000, month=1, day=1, hour=1)

    @property
    def _arbitrary_date_two(self) -> datetime:
        return datetime(year=2000, month=3, day=3, hour=3)

    @property
    def _arbitrary_reservation_with_nonzero_timewindow(self) -> Reservation:
        return Reservation(facility=Facility(angle_of_visibility_cone=0,
                                             point_coordinates=Coordinates(latitude=0, longitude=0),
                                             name='name'),
                           time=TimeWindow(begin=datetime(year=2001, month=2, day=1, hour=1), end=datetime(year=2001, month=2, day=1, hour=6)))


