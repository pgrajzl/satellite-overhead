from sopp.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import EventFinderRhodesmill
from sopp.builder.configuration_builder import ConfigurationBuilder


def main():

    configuration = (
        ConfigurationBuilder()
        .set_facility(
            latitude=40.8178049,
            longitude=-121.4695413,
            elevation=986,
            name='HCRO',
            beamwidth=3,
            bandwidth=10,
            frequency=135
        )
        .set_time_window(
            begin='2023-11-15T08:00:00.0',
            end='2023-11-15T08:30:00.0'
        )
        .set_observation_target(
            declination='7d24m25.426s',
            right_ascension='5h55m10.3s'
        )
        .set_runtime_settings(
            concurrency_level=8,
            time_continuity_resolution=1
        )
        # Alternatively set all of the above settings from a config file
        #.set_from_config_file(config_file_loader='./supplements/config.json')
        .set_satellites(tle_file='./supplements/satellites.tle')
        .build()
    )

    reservation = configuration.reservation

    # Display configuration
    print('\nFinding satellite interference events for:\n')
    print(f'Facility: {reservation.facility.name}')
    print(f'Location: {reservation.facility.coordinates} at elevation '
          f'{reservation.facility.elevation}')
    print(f'Reservation start time: {reservation.time.begin}')
    print(f'Reservation end time: {reservation.time.end}')
    print(f'Observation frequency: {reservation.frequency.frequency} MHz')

    # Determine Satellite Interference
    interference_events = EventFinderRhodesmill(
        list_of_satellites=configuration.satellites,
        reservation=configuration.reservation,
        antenna_direction_path=configuration.antenna_direction_path,
        runtime_settings=configuration.runtime_settings,
    ).get_satellites_crossing_main_beam()

    print('\n==============================================================\n')
    print(f'There are {len(interference_events)} satellite interference\n'
          f'events during the reservation\n')
    print('==============================================================\n')

    for i, window in enumerate(interference_events, start=1):
        max_alt = max(window.positions, key=lambda pt: pt.position.altitude)

        print(f'Satellite interference event #{i}:')
        print(f'Satellite: {window.satellite.name}')
        print(f'Satellite enters view: {window.overhead_time.begin} at '
              f'{window.positions[0].position.azimuth:.2f}')
        print(f'Satellite leaves view: {window.overhead_time.end} at '
              f'{window.positions[-1].position.azimuth:.2f}')
        print(f'Satellite maximum altitude: {max_alt.position.altitude:.2f}')
        print('__________________________________________________\n')


if __name__ == '__main__':
    main()
