from datetime import datetime
import json
import pytz

from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.frequency_filter.frequency_filter import FrequencyFilter
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesMill
from tests.utilities import get_script_directory
from pathlib import Path
from configparser import ConfigParser
from satellite_determination.tle_fetcher import TleFetcher
from satellite_determination.window_finder import WindowFinder

def run_sopp():
    print('Launching Satellite Orbit Preprocessor')
    #routine to check date of last TLE pull
    print('Getting TLE file from space-track.org')
    #TleFetcher().get_tles()
    print('Loading config')
    config_object = ConfigParser()
    config_object.read('.config')
    reservation_parameters = config_object["RESERVATION"]
    start_datetime_str = reservation_parameters["StartTimeUTC"]
    end_datetime_str = reservation_parameters["EndTimeUTC"]
    start_time = datetime.strptime(start_datetime_str, '%m/%d/%y %H:%M:%S %z') #.astimezone(pytz.UTC)
    end_time = datetime.strptime(end_datetime_str, '%m/%d/%y %H:%M:%S %z') #.astimezone(pytz.UTC)
    reservation = Reservation(
        facility=Facility(
            elevation=float(reservation_parameters["Elevation"]),
            point_coordinates=Coordinates(latitude=float(reservation_parameters["Latitude"]), longitude=float(reservation_parameters["Longitude"])),
            name=reservation_parameters["Name"],
            azimuth=float(reservation_parameters["Azimuth"])
        ),
        time=TimeWindow(begin=start_time, end=end_time),
        frequency=FrequencyRange(
            frequency=float(reservation_parameters["Frequency"]),
            bandwidth=float(reservation_parameters["Bandwidth"])
        )
    )
    tle_file = Path(get_script_directory(__file__), 'TLEData', 'arbitrary_TLE.txt')
    frequency_file = Path(get_script_directory(__file__), 'SatList (2).csv')
    satellite_list = Satellite.from_tle_file(tlefilepath=tle_file, frequencyfilepath=frequency_file)
    num_of_sats = len(satellite_list)
    print('loaded ', num_of_sats, ' satellites. Starting frequency filter.')
    frequency_filtered_sats = FrequencyFilter(satellites=satellite_list,
                                              observation_frequency=reservation.frequency).filter_frequencies()
    print(len(frequency_filtered_sats), ' satellites remaining')
    print('Finding interference windows.')
    interference_windows = EventFinderRhodesMill(list_of_satellites=frequency_filtered_sats, reservation=reservation).get_overhead_windows()

    print("=======================================================================================\n")
    print('                     Found ', len(interference_windows), ' interference events in specified reservation')
    print("                               Interference events: \n")
    print("=======================================================================================\n")
    i = 1
    for window in interference_windows:
        print('Interference event #', i, ':')
        print('Satellite:', window.satellite.name)
        print('Satellite enters view: ', window.overhead_time.begin)
        print('Satellite leaves view: ', window.overhead_time.end)
        print('__________________________________________________\n')
        i+=1
    print("=======================================================================================\n")
    print("                       Finding reservation suggestions\n")
    print("=======================================================================================\n")
    suggested_reservation = WindowFinder(reservation, frequency_filtered_sats, EventFinderRhodesMill).find()
    index = 0
    for res in suggested_reservation:
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Reservation suggestion #", index+1)
        print("Suggested start time: ", res.suggested_start_time)
        print("Number of satellites overhead: ", len(res.overhead_satellites))
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        index+=1
    reservation_choice = input("Choose desired reservation number: ")
    index = int(reservation_choice) - 1
    chosen_reservation = suggested_reservation[index]
    chosen_reservation_end_time = chosen_reservation.suggested_start_time + reservation.time.duration
    
    # Open the tardys3 reservation format
    with open('tardys3.json') as f:
        tardys3 = json.load(f)

    # Input data from variables into json file
    tardys3['definitions']['ScheduledEvent']['properties']['dateTimeStart'] = {
    "type": "string",
    "format": "date-time",
    "default": f"{chosen_reservation.suggested_start_time.strftime('%y-%m-%d %H:%M:%S')}"
    }

    tardys3['definitions']['ScheduledEvent']['properties']['dateTimeEnd'] = {
    "type": "string",
    "format": "date-time",
    "default": f"{chosen_reservation_end_time.strftime('%y-%m-%d %H:%M:%S')}"
    }

    # Print the tardys3 reservation file for debugging
    print(tardys3)

    reservation_in_tardys3 = json.dumps(tardys3)
    print(reservation_in_tardys3)
    
    #reservation_in_tardys3 = {
    #    'dateTimeStart': chosen_reservation.suggested_start_time.strftime('%y-%m-%d %H:%M:%S'),
    #    'dateTimeEnd': chosen_reservation_end_time.strftime('%y-%m-%d %H:%M:%S')
    #}
    #with open("tardys3_res.json", "w") as fp:
    #    json.dump(reservation_in_tardys3, fp)

'''
def measure_filtering():
    reservation = Reservation(facility=Facility(elevation=0,
                                                point_coordinates=Coordinates(latitude=0, longitude=0),
                                                name='name', azimuth=30),
                           time=TimeWindow(begin=datetime(year=2001, month=2, day=1, hour=1), end=datetime(year=2001, month=2, day=2, hour=1)),
                           frequency=FrequencyRange(
                               frequency=135,
                               bandwidth=20
                           )
                           )
    tle_file = Path(get_script_directory(__file__), 'TLEData', 'test.txt')
    frequency_file = Path(get_script_directory(__file__), 'SatList (2).csv')
    satellite_list = Satellite.from_tle_file(tlefilepath=tle_file, frequencyfilepath=frequency_file)
    for sat in satellite_list:
        for frequency in sat.frequency:
            print(frequency.frequency)
    print(len(satellite_list))
    frequency_filtered_sats = FrequencyFilter(satellites=satellite_list, observation_frequency=reservation.frequency).filter_frequencies()
    print(len(frequency_filtered_sats))
'''
run_sopp()
