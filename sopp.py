from dataclasses import replace

from sopp.main import Main
from sopp.tle_fetcher.tle_fetcher import TleFetcher
from sopp.builder.configuration_builder import ConfigurationBuilder
from sopp.utilities import get_frequencies_filepath, get_satellites_filepath
from sopp.graph_generator.graph_generator import GraphGenerator


def main():
    print('----------------------------------------------------------------------')
    print('|                                                                    |')
    print('|             Launching Satellite Orbit Preprocessor                 |')
    print('|                                                                    |')
    print('----------------------------------------------------------------------')
    print('Loading reservation parameters from config file...\n')  # make flag to specify config file, default .config
    tle_file = get_satellites_filepath()
    frequency_file = get_frequencies_filepath()

    configuration = (
        ConfigurationBuilder()
        .set_from_config_file()
        .set_satellites(tle_file=tle_file, frequency_file=frequency_file)
        .build()
    )
    reservation = configuration.reservation

    print('Finding satellite interference events for:\n')
    print('Facility: ', reservation.facility.name, ' at ', reservation.facility.coordinates)
    print('Reservation start time: ', reservation.time.begin)
    print('Reservation end time: ', reservation.time.end)
    print('Observation frequency: ', reservation.frequency.frequency, ' MHz')
    print('\n----------------------------------------------------------------------')

    results = Main(antenna_direction_path=configuration.antenna_direction_path,
                   reservation=configuration.reservation,
                   satellites=configuration.satellites).run()

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
