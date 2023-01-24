from skyfield.api import load, wgs84
import datetime
from satellite_determination.dataclasses.reservation import Reservation
from satellite_determination.dataclasses.overhead_window import OverheadWindow
from satellite_determination.retrievers.satellite_retriever.skyfield_satellite_retriever import SkyfieldSatelliteList
from satellite_determination.validator.validator import Validator
from satellite_determination.dataclasses.time_window import TimeWindow
from satellite_determination.utilities import convert_tz_to_utc
from skyfield.timelib import Timescale
from skyfield.api import utc

class ValidatorRhodesMill(Validator):

    def overhead_list(self, list_of_satellites: SkyfieldSatelliteList, reservation: Reservation):
        ts = load.timescale()
        overhead_window_list = [] #list of interferers and when they are interfering as class OverheadWindow
        begin = 0 #variable to store begining timestamps of interference occurences
        end = 0 #variable to store end timestamps
        t0 = ts.utc(convert_tz_to_utc(reservation.time.begin)) #use function in utilities to convert local time to utc
        t1 = ts.utc(convert_tz_to_utc(reservation.time.end))
        coordinates = wgs84.latlon(reservation.facility.point_coordinates.latitude, reservation.facility.point_coordinates.longitude)
        for sat in list_of_satellites.satellites:
            t, events = sat.find_events(coordinates, t0, t1, altitude_degrees=reservation.facility.angle_of_visibility_cone)
            if events.size == 0:
                continue
            else:
                for ti, event in zip(t, events):
                    if event == 0:
                        if end == 0:
                            # last interference occurrence has no end (ends with reservation)
                            # save last interference occurrence
                            end = reservation.time.end
                            time_window = TimeWindow(begin, end)
                            overhead = OverheadWindow(sat, time_window)
                            overhead_window_list.append(overhead)
                        else:
                            # last interference occurrence has end
                            # do nothing
                            continue
                        begin = ti
                        end = 0 #start tracking new interference occurrence
                    elif event == 2:
                        #event 2 in skyfield api is sat leaving overhead. Event we are tracking has end event
                        #so set end to ti of end event and append to interferers
                        end = ti
                        time_window = TimeWindow(begin, end)
                        overhead = OverheadWindow(sat, time_window)
                        overhead_window_list.append(overhead)
        return overhead_window_list

