# S.O.P.P. - Satellite Orbit Prediction Processor

## Quick Start Guide

Welcome to S.O.P.P., an open-source tool for calculating satellite interference in radio astronomy observations.

### Introduction

The SOPP package assists astronomers in optimizing observation scheduling to mitigate radio interference from satellite sources. This is achieved by computing the positions of satellites relative to the observation facility and determining which of these satellites cause interference with the main beam during the observation.

The primary functionality offered by the package is accessed through the `Sopp` class. This class implements two methods:

- `get_satellites_crossing_main_beam`
- `get_satellites_above_horizon`

### High-Level Overview

1. **Define Observation Characteristics:**
   - Provide the necessary observation characteristics to the `ConfigurationBuilder` class:
     - Facility Location
     - Observation Time Window
     - Antenna Frequency and Bandwidth
     - Antenna observation path
     - Satellite TLE data
     - Runtime settings

2. **Determine Satellite Interference:**
   - Create an instance of Sopp using the `Configuration` built by the `ConfigurationBuilder` class.
   - Utilize the methods of the Sopp class to obtain position data of interfering satellites:
     - `get_satellites_crossing_main_beam`: Returns satellites that cross the main beam during observation.
     - `get_satellites_above_horizon`: Returns all satellites above the horizon during the observation.

### Define Observation Characteristics

#### `ConfigurationBuilder`

The observation characteristics must be provided to the `ConfigurationBuilder` class. The configuration builder will then construct a fully prepared `Configuration` object used to determine satellite interference.

An example using `ConfigurationBuilder`:
```python
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
    #.set_from_config_file(config_file='./supplements/config.json')
    .set_satellites(tle_file='./supplements/satellites.tle')
    .build()
)
```

The `ConfigurationBuilder` must call the following methods with the necessary arguments:

- `set_facility()`
- `set_time_window()`
- `set_observation_target()`
- `set_satellites()`
- `set_runtime_settings()`

#### `set_facility()`

The `set_facility()` method specifies the latitude, longitude, elevation (in meters), name, bandwidth, beamwidth and frequency:

```python
configuration.set_facility(
    latitude=40.8178049,
    longitude=-121.4695413,
    elevation=986,
    name='HCRO',
    beamwidth=3,
    bandwidth=10,
    frequency=135
)
```

#### `set_time_window()`

The `set_time_window()` method defines the observation time window in UTC, specifying when the observation will take place. The date format follows the ISO 8601 datetime format: `Y-m-dTH:M:S.f`. The provided datetime string can include microseconds or not. It additionally accepts a time zone, for example, `2023-11-15T08:00:00-7:00`. All times are converted to UTC.

```python
configuration.set_time_window(
    begin='2023-11-15T08:00:00.0',
    end='2023-11-15T08:30:00.0'
)
```

#### `set_observation_target()`

The `set_observation_target()` method defines the target for observation. It has three options:

1. Specify a target by providing its declination and right ascension:

```python
configuration.set_observation_target(
    declination='7d24m25.426s',
    right_ascension='5h55m10.3s'
)
```

2. Specify a static location to observe by providing an azimuth and altitude:

```python
configuration.set_observation_target(
    azimuth=24.2,
    right_ascension=78.1
)
```

3. Provide a custom antenna direction path (how to construct a custom path is explained later):

```python
configuration.set_observation_target(
    custom_path=custom_path
)
```

#### `set_satellites()`

The `set_satellites()` method takes the file path of the satellite TLE data and an optional frequency file. The frequency data can be utilized to filter out satellites whose downlink frequency does not overlap with the observation frequency. This filtering can be disabled if desired.


```python
configuration.set_satellites(
    tle_file='path/to/satellites.tle',
    frequency_file='/path/to/frequency.csv'
)
```

#### `set_runtime_settings()`

The `set_runtime_settings()` method specifies the time resolution for calculating satellite positions in seconds via the `time_continuity_resolution` parameter. Additionally, the `concurrency_level` parameter determines the number of parallel jobs during satellite position calculation, optimizing runtime speeds. This value should be not exceed the number of cores on the machine.

```python
configuration.set_runtime_settings(
    concurrency_level=8,
    time_continuity_resolution=1
)
```

#### `build()`

Finally, once all the required methods have been called use the `build()` method to obtain the `Configuration` object:

```python
configuration = configuration.build()
```

#### `set_from_config_file()`

The `set_from_config_file()` method can be used to provide all of the observation characteristics via a JSON configuration file instead of being set programatically.

```python
configuration = (
    ConfigurationBuilder()
    .set_from_config_file(config_file='./supplements/config.json')
    .set_satellites(tle_file='./supplements/satellites.tle')
    .build()
)
```

The JSON config file follows the following format:
```
{
  "facility": {
    "beamwidth": 3,
    "elevation": 986,
    "latitude": 40.8178049,
    "longitude": -121.4695413,
    "name": "HCRO"
  },
  "frequencyRange": {
    "bandwidth": 10,
    "frequency": 135
  },
  "observationTarget": {
    "declination": "-38d6m50.8s",
    "rightAscension": "4h42m"
  },
  "reservationWindow": {
    "startTimeUtc": "2023-09-27T12:00:00.000000",
    "endTimeUtc": "2023-09-27T13:00:00.000000"
  },
  "runtimeSettings": {
      "concurrency_level": 4,
      "time_continuity_resolution": 1
  }
}
```

### Determine Satellite Interference

#### `Sopp`

The `Sopp` class utilizes the previously created configuration object to identify satellite interference. It is initialized with the `Configuration` obtained from `ConfigurationBuilder`.

```python
event_finder = Sopp(configuration=configuration)
```

Finally, obtain the position data of interfering satellites, run either:

- `get_satellites_crossing_main_beam`: Returns satellites that cross the main beam during observation.
- `get_satellites_above_horizon`: Returns all satellites that are above the horizon during the observation.

```python
interference_events = event_finder.get_satellites_crossing_main_beam()
```

The data is returned as a list of `OverheadWindow`, which is defined as:

```python
class OverheadWindow:
    satellite: Satellite
    positions: List[PositionTime]
```
The `Satellite` class, containins details about the satellite and a list of PositionTime objects. The `PositionTime` dataclass specifies the satellite's position in altitude and azimuth at a discrete point in time. All times are in UTC.

### Using TleFetcher to Obtain TLE File

A TleFetcher class exists that will automatically fetch the latest TLEs from Celestrak or SpaceTrack:

```python
from sopp.tle_fetcher.tle_fetcher_celestrak import TleFetcherCelestrak

fetcher = TleFetcherCelestrak(tle_file_path='path/to/save/satellites.tle')
fetcher.fetch_tles()
```

SpaceTrack is called identically, however you must set the environment variable `IDENTITY` with your username and `PASSWORD` with your password:

```python
from sopp.tle_fetcher.tle_fetcher_spacetrack import TleFetcherSpacetrack

fetcher = TleFetcherSpacetrack(tle_file_path='path/to/save/satellites.tle')
fetcher.fetch_tles()
```

### Providing Custom Path for Observation

Instead of specifying an observation target or static observation with altitude and azimuth a custom path can be provided as a list of `PositionTime` objects.

```python
custom_path = [
    PositionTime(
        position=Position(altitude=.0, azimuth=.1),
        time=datetime(year=2023, month=3, day=30, hour=10, minute=1, tzinfo=pytz.UTC)
    ),
    PositionTime(
        position=Position(altitude=.1, azimuth=.2),
        time=datetime(year=2023, month=3, day=30, hour=10, minute=2, tzinfo=pytz.UTC)
    ),
    PositionTime(
        position=Position(altitude=.2, azimuth=.2),
        time=datetime(year=2023, month=3, day=30, hour=10, minute=3, tzinfo=pytz.UTC)
    ),
]
```

### Example Code

```python
from sopp.sopp import Sopp
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
        #.set_from_config_file(config_file='./supplements/config.json')
        .set_satellites(tle_file='./supplements/satellites.tle')
        .build()
    )

    # Display configuration
    print('\nFinding satellite interference events for:\n')
    print(f'Facility: {configuration.reservation.facility.name}')
    print(f'Location: {configuration.reservation.facility.coordinates} at elevation '
          f'{configuration.reservation.facility.elevation}')
    print(f'Reservation start time: {configuration.reservation.time.begin}')
    print(f'Reservation end time: {configuration.reservation.time.end}')
    print(f'Observation frequency: {configuration.reservation.frequency.frequency} MHz')

    # Determine Satellite Interference
    event_finder = Sopp(configuration=configuration)
    interference_events = event_finder.get_satellites_crossing_main_beam()

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
```
