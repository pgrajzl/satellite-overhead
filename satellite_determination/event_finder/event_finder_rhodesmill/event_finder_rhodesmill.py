from typing import List
from skyfield.api import load, wgs84, Time
from satellite_determination.azimuth_filter.azimuth_filtering import AzimuthFilter
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.event_finder.event_finder_rhodesmill.support.overhead_window_from_events import \
    EventRhodesmill, EventTypesRhodesmill, OverheadWindowFromEvents
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.utilities import convert_timezone_to_utc, convert_datetime_to_utc


class EventFinderRhodesMill:

    def __init__(self, list_of_satellites: List[Satellite], reservation: Reservation):
        self._list_of_satellites = list_of_satellites
        self._reservation = reservation

    def get_overhead_windows(self):
        ts = load.timescale() #provides time objects with the data tables they need to translate between different time scales: the schedule of UTC leap seconds, and the value of ∆T over time.
        overhead_windows = []
        time_start = ts.from_datetime(convert_datetime_to_utc(self._reservation.time.begin)) #changes the reservation datetime to Skyfield Time object
        time_end = ts.from_datetime(convert_datetime_to_utc(self._reservation.time.end))
        coordinates = wgs84.latlon(self._reservation.facility.point_coordinates.latitude, self._reservation.facility.point_coordinates.longitude)
        for sat in self._list_of_satellites:
            rhodesmill_earthsat = sat.to_rhodesmill() #convert from custom satellite class to Rhodesmill EarthSatellite
            event_times, events = rhodesmill_earthsat.find_events(coordinates, time_start, time_end, altitude_degrees=self._reservation.facility.elevation)
            if events.size == 0:
                continue
            else:
                rhodesmill_event_list = []
                for event_time, event in zip(event_times, events):
                    if event == 0:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.ENTERS, satellite=sat, timestamp=event_time.utc_datetime())
                    elif event == 1:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.CULMINATES, satellite=sat, timestamp=event_time.utc_datetime())
                    elif event == 2:
                        translated_event = EventRhodesmill(event_type=EventTypesRhodesmill.EXITS, satellite=sat, timestamp=event_time.utc_datetime())
                    rhodesmill_event_list.append(translated_event)
                overhead_windows += OverheadWindowFromEvents(events=rhodesmill_event_list,
                                                             reservation=self._reservation).get()
        azimuth_filtered_windows = AzimuthFilter(overhead_windows=overhead_windows, reservation=self._reservation).filter_azimuth()
        return azimuth_filtered_windows
