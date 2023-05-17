from dataclasses import replace

from satellite_determination.TLE_fetcher.tle_fetcher import TleFetcher
from satellite_determination.config_file import ConfigFile, TIME_FORMAT
from satellite_determination.custom_dataclasses.frequency_range.support.get_frequency_data_from_csv import \
    GetFrequencyDataFromCsv
from satellite_determination.frequency_filter.frequency_filter import FrequencyFilter
from satellite_determination.custom_dataclasses.satellite.satellite import Satellite
from satellite_determination.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesMill
from satellite_determination.path_finder.observation_path_finder import ObservationPathFinder
from satellite_determination.utilities import get_frequencies_filepath, get_satellites_filepath
from satellite_determination.graph_generator.graph_generator import GraphGenerator


if __name__ == '__main__':
    print('----------------------------------------------------------------------')
    print('|                                                                    |')
    print('|             Launching Satellite Orbit Preprocessor                 |')
    print('|                                                                    |')
    print('----------------------------------------------------------------------')
    print('Loading reservation parameters from config file...\n') #make flag to specify config file, default .config
    config_file = ConfigFile()
    reservation = config_file.reservation
    search_window = config_file.search_window

    print('Finding satellite interference events for:\n')
    print('Facility: ', reservation.facility.name, ' at ', reservation.facility.point_coordinates)
    print('Reservation start time: ', reservation.time.begin)
    print('Reservation end time: ', reservation.time.end)
    print('Observation frequency: ', reservation.frequency.frequency, ' MHz')
    print('\n----------------------------------------------------------------------')
    TleFetcher().get_tles_celestrak()
    tle_file = get_satellites_filepath()
    frequency_file = get_frequencies_filepath()
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
    altitude_azimuth_pairs = ObservationPathFinder(reservation, reservation.time.begin.strftime(TIME_FORMAT), reservation.time.end.strftime(TIME_FORMAT)).calculate_path()
    satellites_above_horizon = EventFinderRhodesMill(list_of_satellites=frequency_filtered_sats, reservation=reservation, azimuth_altitude_path=altitude_azimuth_pairs, search_window=search_window).get_overhead_windows()
    interference_windows = EventFinderRhodesMill(list_of_satellites=frequency_filtered_sats, reservation=reservation, azimuth_altitude_path=altitude_azimuth_pairs, search_window=search_window).get_overhead_windows_slew()
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
    GraphGenerator(search_window_start=search_window.begin, search_window_end=search_window.end, satellites_above_horizon=satellites_above_horizon, interference_windows=interference_windows).generate_graph()
