from sopp.utilities import read_datetime_string_as_utc
from sopp.satellites_loader.satellites_loader_from_files import \
    SatellitesLoaderFromFiles
from sopp.event_finder.event_finder_rhodesmill.event_finder_rhodesmill import \
    EventFinderRhodesmill
from sopp.path_finder.observation_path_finder_rhodesmill import \
    ObservationPathFinderRhodesmill
from sopp.custom_dataclasses.observation_target import ObservationTarget
from sopp.custom_dataclasses.facility import Facility
from sopp.custom_dataclasses.coordinates import Coordinates
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.runtime_settings import RuntimeSettings
from sopp.custom_dataclasses.frequency_range.frequency_range import \
    FrequencyRange
from sopp.frequency_filter.frequency_filter import FrequencyFilter
from datetime import timedelta


def main():
    # Facility
    facility = Facility(
        Coordinates(
            latitude=40.8178049,
            longitude=-121.4695413,
        ),
        elevation=986,  # meters
        beamwidth=3,    # degrees
        name='HCRO',
    )

    # Observation Window
    time_window = TimeWindow(
        begin=read_datetime_string_as_utc('2023-11-15T08:00:00.000000'),
        end=read_datetime_string_as_utc('2023-11-15T08:30:00.000000'),
    )

    # Frequency Range
    frequency_range = FrequencyRange(bandwidth=10, frequency=135)

    # Reservation
    reservation = Reservation(
        facility=facility,
        time=time_window,
        frequency=frequency_range
    )

    # Specify Observation Target
    observation_target = ObservationTarget(
        declination='7d24m25.426s',
        right_ascension='5h55m10.3s'
    )

    # Antenna Direction Path (going to do automatically)
    antenna_direction_path = ObservationPathFinderRhodesmill(
        facility,
        observation_target,
        time_window
    ).calculate_path()

    # Load Satellites
    all_satellites = SatellitesLoaderFromFiles(
        tle_file='./satellites.tle',
    ).load_satellites()

    # Filter satellites on frequency (optional, going to do automatically)
    filtered_satellites = FrequencyFilter(
        satellites=all_satellites,
        observation_frequency=frequency_range
    ).filter_frequencies()

    # Runtime Settings
    runtime_settings = RuntimeSettings(
        concurrency_level=8,
        time_continuity_resolution=timedelta(seconds=1)
    )

    # Display configuration
    print('\nFinding satellite interference events for:\n')
    print(f'Facility: {reservation.facility.name}')
    print(f'Location: {reservation.facility.coordinates} at elevation '
          f'{reservation.facility.elevation}')
    print(f'Reservation start time: {reservation.time.begin}')
    print(f'Reservation end time: {reservation.time.end}')
    print(f'Observation frequency: {reservation.frequency.frequency} MHz')
    print(f'Observing celestial object at: '
          f'Declination: {observation_target.declination} '
          f'Right Ascension:{observation_target.right_ascension}')

    # Determine Satellite Interference
    interference_events = EventFinderRhodesmill(
        list_of_satellites=filtered_satellites,
        reservation=reservation,
        antenna_direction_path=antenna_direction_path,
        runtime_settings=runtime_settings,
    ).get_satellites_crossing_main_beam()

    ########################################################################

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
