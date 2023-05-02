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
from satellite_determination.path_finder.observation_path_finder import ObservationPathFinder
from satellite_determination.utilities import get_script_directory
from pathlib import Path
from configparser import ConfigParser
from satellite_determination.graph_generator.graph_generator import GraphGenerator

SUPPLEMENTS_DIRECTORY = Path(get_script_directory(__file__), 'supplements')


if __name__ == '__main__':
    print('----------------------------------------------------------------------')
    print('|                                                                    |')
    print('|             Launching Satellite Orbit Preprocessor                 |')
    print('|                                                                    |')
    print('----------------------------------------------------------------------')
    print('Loading reservation parameters from config file...\n') #make flag to specify config file, default .config
    config_object = ConfigParser()
    config_object.read(Path(SUPPLEMENTS_DIRECTORY, '.config'))
    reservation_parameters = config_object["RESERVATION"]
    start_datetime_str = reservation_parameters["StartTimeUTC"]
    end_datetime_str = reservation_parameters["EndTimeUTC"]
    search_window_start_str = reservation_parameters["SearchWindowStart"]
    search_window_end_str = reservation_parameters["SearchWindowEnd"]
    start_time = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M:%S.%f')
    end_time = datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M:%S.%f')
    search_window_start = datetime.strptime(search_window_start_str, '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=pytz.UTC)
    search_window_end = datetime.strptime(search_window_end_str, '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=pytz.UTC)
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

    tle_file = Path(SUPPLEMENTS_DIRECTORY, 'active_sats.tle')
    frequency_file = Path(get_script_directory(__file__), 'satellite_determination/SatList (2).csv')
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
    satellites_above_horizon = EventFinderRhodesMill(list_of_satellites=frequency_filtered_sats, reservation=reservation, azimuth_altitude_path=altitude_azimuth_pairs, search_time_start=search_window_start, search_time_end=search_window_end).get_overhead_windows()
    interference_windows = EventFinderRhodesMill(list_of_satellites=frequency_filtered_sats, reservation=reservation, azimuth_altitude_path=altitude_azimuth_pairs, search_time_start=search_window_start, search_time_end=search_window_end).get_overhead_windows_slew()
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
    GraphGenerator(search_window_start=search_window_start, search_window_end=search_window_end, satellites_above_horizon=satellites_above_horizon, interference_windows=interference_windows).generate_graph()
