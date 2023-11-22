from dataclasses import replace

from satellite_determination.tle_fetcher.tle_fetcher import TleFetcher
from satellite_determination.config_file.config_file_factory import get_config_file_object
from satellite_determination.dataclasses.configuration import Configuration
from satellite_determination.dataclasses.frequency_range.support.get_frequency_data_from_csv import \
    GetFrequencyDataFromCsv
from satellite_determination.dataclasses.position_time import PositionTime
from satellite_determination.dataclasses.satellite.satellite import Satellite
from satellite_determination.main import Main
from satellite_determination.path_finder.observation_path_finder import ObservationPathFinder
from satellite_determination.utilities import get_frequencies_filepath, get_satellites_filepath
from satellite_determination.graph_generator.graph_generator import GraphGenerator
from satellite_determination.variable_initializer.variable_initializer_from_config import VariableInitializerFromConfig
from satellite_determination.satellites_loader.satellites_loader_from_files import SatellitesLoaderFromFiles


def main():
    print('----------------------------------------------------------------------')
    print('|                                                                    |')
    print('|             Launching Satellite Orbit Preprocessor                 |')
    print('|                                                                    |')
    print('----------------------------------------------------------------------')
    print('Loading reservation parameters from config file...\n')  # make flag to specify config file, default .config
    config_file = get_config_file_object()
    tle_file = get_satellites_filepath()
    frequency_file = get_frequencies_filepath()
    satellites_loader = SatellitesLoaderFromFiles(tle_file=tle_file, frequency_file=frequency_file)
    var_initializer = VariableInitializerFromConfig(satellites_loader=satellites_loader, config=config_file.configuration)
    reservation = var_initializer.get_reservation()

    print('Finding satellite interference events for:\n')
    print('Facility: ', reservation.facility.name, ' at ', reservation.facility.coordinates)
    print('Reservation start time: ', reservation.time.begin)
    print('Reservation end time: ', reservation.time.end)
    print('Observation frequency: ', reservation.frequency.frequency, ' MHz')
    print('\n----------------------------------------------------------------------')

    results = Main(antenna_direction_path=var_initializer.get_antenna_direction_path(),
                   reservation=var_initializer.get_reservation(),
                   satellites=var_initializer.get_satellite_list()).run()

    print("=======================================================================================\n")
    print('       Found ', len(results.interference_windows), ' instances of satellites crossing the main beam.')
    print('    There are ', len(results.satellites_above_horizon), ' satellites above the horizon during the reservation')
    print("                      Main Beam Interference events: \n")
    print("=======================================================================================\n")
    i = 1
    for window in results.interference_windows:
        print('Interference event #', i, ':')
        print('Satellite:', window.satellite.name)
        print('Satellite enters view: ', window.overhead_time.begin)
        print('Satellite leaves view: ', window.overhead_time.end)
        print('__________________________________________________\n')
        i += 1
    GraphGenerator(search_window_start=reservation.time.begin,
                   search_window_end=reservation.time.end,
                   satellites_above_horizon=results.satellites_above_horizon,
                   interference_windows=results.interference_windows).generate_graph()


if __name__ == '__main__':
    frequencies_filepath = get_satellites_filepath()
    if frequencies_filepath.exists():
        main()
    else:
        TleFetcher().get_tles_celestrak()
        try:
            main()
        finally:
            frequencies_filepath.unlink(missing_ok=True)
