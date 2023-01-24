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
    ENTERS = auto()
    EXITS = auto()


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
        enter_events, exit_events = ([event for event in self._events if event.event_type == event_type]
                                     for event_type in EventTypesRhodesmill)
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

        # for sat in list_of_satellites.satellites:
        #     t, events = sat.find_events(coordinates, t0, t1, altitude_degrees=reservation.facility.angle_of_visibility_cone)
        #
        #     for ti, event in zip(t, events):
        #         if event == 0:
        #             if end == 0:
        #                 # last interference occurrence has no end (ends with reservation)
        #                 # save last interference occurrence
        #                 end = reservation.time.end
        #                 time_window = TimeWindow(begin=begin, end=end)
        #                 overhead = OverheadWindow(sat, time_window)
        #                 overhead_window_list.append(overhead)
        #             else:
        #                 # last interference occurrence has end
        #                 # do nothing
        #                 continue
        #             begin = ti
        #             end = 0 #start tracking new interference occurrence
        #         elif event == 2:
        #             #event 2 in skyfield api is sat leaving overhead. Event we are tracking has end event
        #             #so set end to ti of end event and append to interferers
        #             end = ti
        #             time_window = TimeWindow(begin, end)
        #             overhead = OverheadWindow(sat, time_window)
        #             overhead_window_list.append(overhead)
        # return overhead_window_list

    @property
    def _arbitrary_satellite(self) -> Satellite:
        return Satellite(name='name')

    @property
    def _arbitrary_date(self) -> datetime:
        return datetime(year=2000, month=1, day=1)

    @property
    def _arbitrary_reservation_with_nonzero_timewindow(self) -> Reservation:
        return Reservation(facility=Facility(angle_of_visibility_cone=0,
                                             point_coordinates=Coordinates(latitude=0, longitude=0),
                                             name='name'),
                           time=TimeWindow(begin=datetime.now(), end=datetime.now() + timedelta(days=1)))
