# S.O.P.P. - Satellite Orbit Prediction Processor

## Quick Start Guide

Welcome to S.O.P.P., an open-source tool for calculating satellite interference in radio astronomy observations.

### Introduction

The SOPP package assists astronomers in optimizing observation scheduling to mitigate radio interference from satellite sources. This is achieved by computing the positions of satellites relative to the observation facility and determining which of these satellites cause interference with the main beam during the observation.

The primary functionality offered by the package is accessed through the `EventFinderRhodesmill` class. This class implements two methods:

- `get_satellites_crossing_main_beam`
- `get_satellites_above_horizon`

### High-Level Overview

1. **Define Observation Characteristics:**
   - Define the necessary data classes to represent observation characteristics:
     - Facility
     - TimeWindow
     - FrequencyRange
     - Reservation
     - ObservationTarget
     - ObservationPathFinder

2. **Load Satellite Data:**
   - Use the SatellitesLoaderFromFiles class to load satellite TLE and optional frequency data.

3. **Determine Satellite Interference:**
   - Create an instance of EventFinderRhodesmill using the loaded satellite data and defined observation characteristics.
   - Utilize the methods of the EventFinderRhodesmill class to obtain position data of interfering satellites:
     - `get_satellites_crossing_main_beam`: Returns satellites that cross the main beam during observation.
     - `get_satellites_above_horizon`: Returns all satellites above the horizon during the observation.

### Define Observation Characteristics

##### Facility

The [Facility](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/custom_dataclasses/facility.py) class defines the geographical location of the observation. It is initialized with four parameters: `Coordinates`, which includes `latitude` and `longitude`, along with `elevation`, `beamwidth`, and an optional `name`.

```python
facility = Facility(
    Coordinates(
        latitude=40.8178049,
        longitude=-121.4695413
    ),
    elevation=986, # meters
    beamwidth=3, # degrees
    name='HCRO'
)
```

##### TimeWindow

The [TimeWindow](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/custom_dataclasses/time_window.py) class defines the observation time window, specifying when the observation will take place. It is initialized with two [datetime](https://docs.python.org/3/library/datetime.html) parameters: `begin` and `end`. `read_datetime_string_as_utc` serves as an utility function to easily construct a datetime.

```python
time_window = TimeWindow(
    begin=read_datetime_string_as_utc('2023-11-12T09:00:00.000000'),
    end=read_datetime_string_as_utc('2023-11-12T10:00:00.000000')
)
```

##### FrequencyRange

The [FrequencyRange](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/custom_dataclasses/frequency_range/frequency_range.py) class defines the frequency of the observation. It is initialized with two parameters, the frequency and bandwidth:

```python
frequency_range = FrequencyRange(frequency=128, bandwidth=10)
```

##### Reservation

The [Reservation](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/custom_dataclasses/reservation.py) class encapsulates the `Facility`, `TimeWindow` and `FrequencyRange`. 

```python
reservation = Reservation(
    facility=facility,
    time=time_window,
    frequency=frequency_range
)
```

##### ObservationTarget

The [ObservationTarget](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/custom_dataclasses/observation_target.py) class specifies the target for observation, initialized with two parameters: `declination` and `right_ascension`.

```python
observation_target = ObservationTarget(declination='7d24m25.426s', right_ascension='5h55m10.3s')
```

##### ObservationPathFinder

The [ObservationPathFinder](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/path_finder/observation_path_finder.py) class utilizes the previously created `ObservationTarget`, `Facility`, and `TimeWindow` to generate an antenna direction path. The antenna direction path is a list of `PositionTime` objects, capturing each minute within the observation window with the antenna's current altitude and azimuth coordinates.

```python
antenna_direction_path = ObservationPathFinderRhodesmill(
    facility=facility,
    observation_target=observation_target,
    time_window=time_window
).calculate_path()
```
Alternatively, instead of specifying an observation target and utilizing the PathFinder class to generate the antenna direction path, you can provide a custom antenna path as a list of `PositionTime` objects.

### Load Satellite Data

##### SatellitesLoaderFromFiles

The [SatellitesLoaderFromFiles](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/satellites_loader/satellites_loader_from_files.py) class loads a list of satellites from files. It is initialized with two parameters, `tle_file`, as the satellite TLE file path and an optional frequency file path in parameter `frequency_file`:

```python
list_of_satellites = SatellitesLoaderFromFiles(tle_file='./satellites.tle', frequency_file='./frequency_data.csv').load()
```

The optional frequency file can be provided as a `.csv` file. If frequency data is available, the [Satellite](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/custom_dataclasses/satellite/satellite.py) class will be populated with the relevant frequency information.

Furthermore, the frequency data can be utilized to filter out satellites whose downlink frequency does not overlap with the observation frequency. This filtering process is facilitated by the [FrequencyFilter](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/frequency_filter/frequency_filter.py) class:

```python
filtered_satellites = FrequencyFilter(
    satellites=list_of_satellites,
    observation_frequency=frequency_range
).filter_frequencies()
```

### Determine Satellite Interference

##### RuntimeSettings

The [RuntimeSettings](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/custom_dataclasses/runtime_settings.py) class serves as an optional parameter for the `EventFinderRhodesmill` class. The parameter `time_continuity_resolution` specifies the time resolution, as a [timedelta](https://docs.python.org/3/library/datetime.html#timedelta-objects), for calculating satellite positions, with a default of 1 second. Additionally, the `concurrency_level` parameter determines the number of parallel jobs during satellite position calculation, optimizing runtime speeds. This value should be approximately equivalent to the number of cores on the machine.

```python
runtime_settings = RuntimeSettings(
    concurrency_level=8,
    time_continuity_resolution=timedelta(seconds=1)
)
```

##### EventFinderRhodesmill

The [EventFinderRhodesmill](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/event_finder/event_finder.py) class utilizes the previously created data classes to identify satellite interference. It is initialized with the `list_of_satellites` obtained from `SatellitesLoaderFromFiles`, `reservation`, `antenna_direction_path`, and an optional `runtime_settings`.

```python
event_finder = EventFinderRhodesmill(
    list_of_satellites=list_of_satellites,
    reservation=reservation,
    antenna_direction_path=antenna_direction_path,
    runtime_settings=runtime_settings
)
```

Finally, obtain the position data of interfering satellites, run either:

- `get_satellites_crossing_main_beam`: Returns satellites that cross the main beam during observation.
- `get_satellites_above_horizon`: Returns all satellites that are above the horizon during the observation.

```python
interference_events = event_finder.get_satellites_crossing_main_beam()
```

The data is returned as a list of [OverheadWindow](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/custom_dataclasses/overhead_window.py). Which is defined as: 

```python
class OverheadWindow:
    satellite: Satellite
    positions: List[PositionTime]
```
The `Satellite` class, containins details about the satellite and a list of [PositionTime](https://github.com/NSF-Swift/satellite-overhead/blob/main/satellite_determination/custom_dataclasses/position_time.py) objects. The `PositionTime` dataclass specifies the satellite's position in altitude and azimuth at a discrete point in time.



