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
    ENTERS = auto() #Skyfield API returns events as 0, 1, or 2 for enters, culminates, exits
    EXITS = auto()


@dataclass
class EventRhodesmill:
    event_type: EventTypesRhodesmill
    timestamp: datetime


class TimeWindowsFromEvents:
    def __init__(self, events: List[EventRhodesmill], time_endpoints: TimeWindow):
        self._events = events
        self._time_endpoints = time_endpoints

    def get(self) -> List[TimeWindow]:
        enter_events, exit_events = ([event for event in self._events if event.event_type == event_type]
                                     for event_type in EventTypesRhodesmill)
        if len(enter_events) != len(exit_events): #Handle case where a satellite starts or ends in observation area
            if self._events[0].event_type == EventTypesRhodesmill.ENTERS: #the first event is the satellite entering view, so it didn't start in observation area
                end_reservation_event = EventRhodesmill(event_type=EventTypesRhodesmill.EXITS, timestamp=self._time_endpoints.end)
                exit_events.append(end_reservation_event)
            elif self._events[0].event_type == EventTypesRhodesmill.EXITS: #the first event is an exit, so the sat starts in view
                start_reservation_event = EventRhodesmill(event_type=EventTypesRhodesmill.ENTERS, timestamp=self._time_endpoints.begin)
                enter_events.insert(0, start_reservation_event)
        enter_and_exit_pairs = zip(enter_events, exit_events)
        return [TimeWindow(begin=begin_event.timestamp, end=exit_event.timestamp) for begin_event, exit_event in
                enter_and_exit_pairs]


class TestOverheadWindowFromEvents:
    def test_one_satellite_only_leaves(self):
        event = EventRhodesmill(
            event_type=EventTypesRhodesmill.EXITS,
            timestamp=self._arbitrary_date
        )
        time_windows = TimeWindowsFromEvents(events=[event], time_endpoints=self._nonzero_timewindow).get()
        assert time_windows == [
            TimeWindow(
                begin=self._nonzero_timewindow.begin,
                end=event.timestamp
            )
        ]

    def test_one_satellite_only_enters(self):
        event = EventRhodesmill(
            event_type=EventTypesRhodesmill.ENTERS,
            timestamp=self._arbitrary_date
        )
        time_windows = TimeWindowsFromEvents(events=[event], time_endpoints=self._nonzero_timewindow).get()
        assert time_windows == [
            TimeWindow(
                begin=event.timestamp,
                end=self._nonzero_timewindow.end
            )
        ]

    def test_one_satellite_enters_and_leaves(self):
        events = {
            EventTypesRhodesmill.ENTERS: EventRhodesmill(
                event_type=EventTypesRhodesmill.ENTERS,
                timestamp=self._arbitrary_date
            ),
            EventTypesRhodesmill.EXITS: EventRhodesmill(
                event_type=EventTypesRhodesmill.EXITS,
                timestamp=self._arbitrary_date + timedelta(hours=1)
            ),
        }
        time_windows = TimeWindowsFromEvents(events=list(events.values()), time_endpoints=self._nonzero_timewindow).get()
        assert time_windows == [
            TimeWindow(
                begin=events[EventTypesRhodesmill.ENTERS].timestamp,
                end=events[EventTypesRhodesmill.EXITS].timestamp
            )
        ]

    def test_one_satellite_enters_and_leaves_twice(self):
        events = [
            EventRhodesmill(
                event_type=EventTypesRhodesmill.ENTERS,
                timestamp=self._arbitrary_date
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.EXITS,
                timestamp=self._arbitrary_date + timedelta(hours=1)
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.ENTERS,
                timestamp=self._arbitrary_date_two
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.EXITS,
                timestamp=self._arbitrary_date_two + timedelta(hours=1)
            ),
        ]
        time_windows = TimeWindowsFromEvents(events=events, time_endpoints=self._nonzero_timewindow).get()
        assert time_windows == [
            TimeWindow(
                begin=events[0].timestamp,
                end=events[1].timestamp
            ),
            TimeWindow(
                begin=events[2].timestamp,
                end=events[3].timestamp
            )
        ]

    def test_one_satellite_enters_leaves_enters(self):
        events = [
            EventRhodesmill(
                event_type=EventTypesRhodesmill.ENTERS,
                timestamp=self._arbitrary_date
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.EXITS,
                timestamp=self._arbitrary_date + timedelta(hours=1)
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.ENTERS,
                timestamp=self._arbitrary_date_two
            ),
        ]
        time_windows = TimeWindowsFromEvents(events=events, time_endpoints=self._nonzero_timewindow).get()
        assert time_windows == [
            TimeWindow(
                begin=events[0].timestamp,
                end=events[1].timestamp
            ),
            TimeWindow(
                begin=events[2].timestamp,
                end=self._nonzero_timewindow.end
            )
        ]

    def test_one_satellite_leaves_enters_leaves(self):
        events = [
            EventRhodesmill(
                event_type=EventTypesRhodesmill.EXITS,
                timestamp=self._arbitrary_date
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.ENTERS,
                timestamp=self._arbitrary_date + timedelta(hours=1)
            ),
            EventRhodesmill(
                event_type=EventTypesRhodesmill.EXITS,
                timestamp=self._arbitrary_date + timedelta(hours=2)
            ),
        ]
        time_windows = TimeWindowsFromEvents(events=events, time_endpoints=self._nonzero_timewindow).get()
        assert time_windows == [
            TimeWindow(
                begin=self._nonzero_timewindow.begin,
                end=events[0].timestamp
            ),
            TimeWindow(
                begin=events[1].timestamp,
                end=events[2].timestamp
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
    def _nonzero_timewindow(self) -> TimeWindow:
        return TimeWindow(begin=datetime(year=2001, month=2, day=1, hour=1), end=datetime(year=2001, month=2, day=1, hour=6))


