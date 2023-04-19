from dataclasses import replace
from datetime import datetime
import pytz
from satellite_determination.custom_dataclasses.coordinates import Coordinates
from satellite_determination.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from satellite_determination.custom_dataclasses.frequency_range.support.get_frequency_data_from_csv import \
    GetFrequencyDataFromCsv
from satellite_determination.custom_dataclasses.time_window import TimeWindow
from satellite_determination.frequency_filter.frequency_filter import FrequencyFilter
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.custom_dataclasses.reservation import Reservation
from satellite_determination.custom_dataclasses.facility import Facility
from satellite_determination.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesMill
from satellite_determination.generate_tardys3 import Tardys3Generator
from satellite_determination.path_finder.observation_path_finder import ObservationPathFinder
from tests.utilities import get_script_directory
from pathlib import Path
from configparser import ConfigParser
from satellite_determination.window_finder import WindowFinder


if __name__ == '__main__':
    print('----------------------------------------------------------------------')
    print('|                                                                    |')
    print('|             Launching Satellite Orbit Preprocessor                 |')
    print('|                                                                    |')
    print('----------------------------------------------------------------------')
    #print('Launching Satellite Orbit Preprocessor')
    print('Loading reservation parameters from config file...\n') #make flag to specify config file, default .config
    config_object = ConfigParser()
    config_object.read('.config')
    reservation_parameters = config_object["RESERVATION"]
    start_datetime_str = reservation_parameters["StartTimeUTC"]
    end_datetime_str = reservation_parameters["EndTimeUTC"]
    #start_time = datetime.strptime(start_datetime_str, '%m/%d/%y %H:%M:%S %z')
    #end_time = datetime.strptime(end_datetime_str, '%m/%d/%y %H:%M:%S %z')
    start_time = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M:%S.%f')
    end_time = datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M:%S.%f')
    reservation = Reservation(
        facility=Facility(
            right_ascension=reservation_parameters["RightAscension"],
            point_coordinates=Coordinates(latitude=float(reservation_parameters["Latitude"]), longitude=float(reservation_parameters["Longitude"])),
            name=reservation_parameters["Name"],
            declination=reservation_parameters["Declination"],
        ),
        time=TimeWindow(begin=start_time, end=end_time),
        frequency=FrequencyRange(
            frequency=float(reservation_parameters["Frequency"]),
            bandwidth=float(reservation_parameters["Bandwidth"])
        )
    )

    print('Finding satellite interference events for:\n')
    print('Facility: ', reservation.facility.name, ' at ', reservation.facility.point_coordinates)
    print('Reservation start time: ', reservation.time.begin)
    print('Reservation end time: ', reservation.time.end)
    print('Observation frequency: ', reservation.frequency.frequency, ' MHz')
    print('\n----------------------------------------------------------------------')

    tle_file = Path(get_script_directory(__file__), 'TLEData', 'active_sats.txt')
    frequency_file = Path(get_script_directory(__file__), 'SatList (2).csv')
    satellite_list = Satellite.from_tle_file(tlefilepath=tle_file)
    frequency_list = GetFrequencyDataFromCsv(filepath=frequency_file).get()
    satellite_list_with_frequencies = [replace(satellite, frequency=frequency_list.get(satellite.tle_information.satellite_number, []))
                                       for satellite in satellite_list]

    num_of_sats = len(satellite_list_with_frequencies)
    print('Loaded ', num_of_sats, ' satellites from TLE file.\nStarting frequency filter.')
    frequency_filtered_sats = FrequencyFilter(satellites=satellite_list_with_frequencies,
                                              observation_frequency=reservation.frequency).filter_frequencies()
    print(len(frequency_filtered_sats), ' satellites remaining of ', num_of_sats, '\n')
    print('Finding interference windows.')
    #test
    altitude_azimuth_pairs = ObservationPathFinder(reservation, start_datetime_str, end_datetime_str).calculate_path()
    satellites_above_horizon = EventFinderRhodesMill(list_of_satellites=frequency_filtered_sats, reservation=reservation, azimuth_altitude_path=altitude_azimuth_pairs).get_overhead_windows()
    interference_windows = EventFinderRhodesMill(list_of_satellites=frequency_filtered_sats, reservation=reservation, azimuth_altitude_path=altitude_azimuth_pairs).get_overhead_windows_slew()
    # test
    print("=======================================================================================\n")
    print('       Found ', len(interference_windows), ' instances of satellites crossing the main beam.')
    print('    There are ', len(satellites_above_horizon), ' satellites above the horizon during the reservation')
    print("                      Main Beam Interference events: \n")
    print("=======================================================================================\n")
    i = 1
    for window in interference_windows:
        print('Interference event #', i, ':')
        print('Satellite:', window.satellite.name)
        print('Satellite enters view: ', window.overhead_time.begin)
        print('Satellite leaves view: ', window.overhead_time.end)
        print('__________________________________________________\n')
        i+=1


'''
    print("=======================================================================================\n")
    print("                       Finding reservation suggestions\n")
    print("=======================================================================================\n")
    suggested_reservation = WindowFinder(reservation, frequency_filtered_sats, EventFinderRhodesMill).search()
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
    Tardys3Generator(chosen_reservation, chosen_reservation_end_time).generate_tardys()'''
