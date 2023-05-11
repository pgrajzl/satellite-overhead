# S.O.P.P. - Satellite Orbit Prediction Processor

SOPP is an open-source tool for calculating satellite interference to radio astronomy observations.

![alt text]

## Running SOPP

### Install the requirements:
```bash
>> pip3 install -r requirements.txt
```

### Setting up the supplemental files

#### Active Satellites TLE File
There should be a [TLE](https://en.wikipedia.org/wiki/Two-line_element_set) file, containing the satellites that you 
want to search through, at `supplements/satellites.tle` under the root directory. If you do not specify a config
file, SOPP will download a list of TLEs from Space-trak.org

#### Config file
There should be a file at `supplements/.config` under the root directory to set default observation values for a reservation. 
The following is an example of a config file:

    [RESERVATION]
    Latitude = 40.8178049
    Longitude = -121.4695413
    RightAscension = 4h42m
    Declination = -38d6m50.8s
    Beamwidth = 3
    Name = HCRO
    StartTimeUTC = 2023-03-30T10:00:00.000000
    EndTimeUTC = 2023-03-30T15:00:00.000000
    Frequency = 135
    Bandwidth = 10

### Run command
In the root directory, run the following command:

```bash
python3 sopp.py
```

## Docker
Run the following commands from the root directory

### Build

```bash
docker build . -t sopp
```

### Run
In the following command
   - `<PATH_TO_LOCAL_SUPPLEMENTAL_DIRECTORY>` should be replaced by the path to a local directory that
     contains two files with the following names:
      - `active_satellites.tle`: contents described in section #active-satellites-tle-file.
      - `.config`: contents described in section #config-file section.

```bash
docker run 
  -v "<PATH_TO_LOCAL_SUPPLEMENTAL_DIRECTORY>:/satellite_orbit_prediction/supplements" \
  sopp
```

## SOPP Components
### Third-Party Tools
- **Space-Track:** [Space-Track.org](https://www.space-track.org) is a site maintained by the U.S. Space Force that allows users to query a database and download satellite TLEs. SOPP contains the functionality to pull satellite TLEs from Space-Track for use in the program, but the site requires users to have an account.
- **Celestrak:** [Celestrak](celestrak.org) is the precursor to space-track and is available without an account. While it has been predicted to be phased out for years, it is still actively maintained. It also has an easily downloadable list of active satellites, which doesn’t include space debris.
- **Astropy:** [Astropy](https://www.astropy.org/) is a Python package designed for use in astronomy and contains functions for many space math problems. Astropy is used in the SOPP tool to calculate the path of an observation target through the sky to determine the telescope’s movement as a function of time. These azimuth and elevation values are then used to determine if a satellite’s movement intersects with this path.
- **Rhodesmill Skyfield:** The [Skyfield API](https://rhodesmill.org/skyfield/) is a comprehensive Python package for computing the positions of stars, planets, and satellites. SOPP uses the Skyfield API to find all the satellites visible above the horizon during an observation search window.
- **Auxiliary Frequency Database:** a satellite frequency database was created by scraping frequency information from various open sources. The code used to generated the database can be found [here](https://github.com/NSF-Swift/sat-frequency-scraper).

### Custom Data Classes
+ **Coordinates**: latitude and longitude
  + *latitude*: float
  + *longitude*: float
+ **TimeWindow**: start and end time for an event
  + *begin*: time event begins. datetime.
  + *end*: time event ends. datetime.
  + *duration(self)*: calculates the total duration of the event and returns a timedelta
  + *overlaps(self, TimeWindow)*: calculates if two TimeWindows overlap
+ **FrequencyRange**: stores a frequency for an observation or satellite transmission
  + *frequency*: center frequency
  + *bandwidth*: bandwidth
  + *status*: status of the antenna (inactive, active, etc) for use understanding if satellite's are transmitting or not.
  + *overlaps(self, FrequencyRange)*: determines if two frequency ranges overlap
+ **Facility**: The Facility data class contains the observation parameters of the facility and the object it is tracking, including coordinates of the RA telescope and its beamwidth, as well as the right ascension and declination values for its observation target.
  + *point_coordinates*: latitude and longitude of RA facility. From custom data class Coordinates in custom_dataclasses/coordinates.py
  + *name*: (optional) name of the facility. String.
  + *right_ascension*: (optional) the right ascension of the observation target. This is not needed if you are performing an observation in a stationary position and the telescope will not slew. String.
  + *declination*: (optional) the declination of the observation target. This is not needed if you are performing an observation in a stationary position and the telescope will not slew. String.
  + *beamwidth:* (optional) beamwidth of the telescope. This is optional and will assign a default value of 3 if left unassigned. float.
  + *height*: (optional) height of the telescope. float.
  + *azimuth*: (optional) azimuth of the telescope. Only used if performing an observation in a stationary position so not often needed. float.
  + *elevation:* (optional) elevation (altitude) of the telescope. Only used if performing an observation in a stationary position so not often needed. float.
+ **Satellite**: the satellite data class stores all of the TLE information for each satellite, which is loaded from a TLE file using the class method from_tle_file() and can be converted to a Skyfield API object EarthSatellite using the to_rhodesmill() method. It also stores all the frequency information for each satellite.
  + *name:* name of satellite. string.
  + *tle_information:* stores TLE information. TleInformation is another custom object to store TLE data and can be found in ~/custom_dataclasses/satellite/tle_information.py
  + *frequency:* list of type FrequencyRange. FrequencyRange is a custom dataclass that stores a center frequency and bandwidth.
  + *to_rhodesmill():* class method to convert a Satellite object into a Rhodemill-Skyfield EarthSatellite object for use with the Skyfield API
  + *from_tle_file()*: class method to load Satellite from provided TLE file. Returns a list of type Satellite.
+ **Reservation:** stores the Facility, as well as some additional reservation-specific information, such as reservation start and end times.
  + *facility*: Facility (see above)
  + *time*: TimeWindow that contains the start and end time of the ideal reservation. Type TimeWindow (see above).
  + *frequency*: frequency of the requested observation. Type FrequencyRange.
+ **OverheadWindow:** designed to store the time windows that a given satellite is overhead and includes the Satellite object, as well as a TimeWindow object that contains the interference start and end times.
  + *satellite*: the satellite that is overhead during the time window. Type Satellite.
  + *overhead_time*: the time the satellite enters and exits view. TimeWindow.
+ **ObservationPath:** represents the telescope's position as a function of time by storing an altitude, azimuth, and timestamp
  + *altitude*: altitude of the telescope. Angle (type from Astropy).
  + *azimuth*: azimuth of the telescope. Angle (from Astropy).
  + *time*: time at which the telescope is at the stored altitude and azimuth. datetime.
### Functional Modules

+ **EventFinder:** EventFinder is the module that determines if a satellite interferes with an RA observation. It has three main functions:
  + *get_overhead_windows_slew():* determines if a satellite crosses the main beam as the telescope moves across the sky by looking for intersections of azimuth and altitude and returning a list of OverheadWindows for events where this occurs
  + *get_overhead_windows():* dDetermines the satellites visible above the horizon during the search window and returns a list of OverheadWindows for each event
  + *track_satellite():* tracks a specific satellite, or list of satellites, and returns the times when its visible from the facility and the azimuth and altitude at which to observe it from
+ **FrequencyFilter:** determines if a satellite's downlink transmission frequency overlaps with the observation frequency and returns a list of Satellite objects with only the satellites that will interfere with the observation.
+ **PathFinder:** determines the path the telescope will need to move to track its target and returns a list of altitude, azimuth, and timestamp to represent this telescope movement
+ **GraphGenerator**: generates bar graphs showing when satellites cross the main beam and how many total satellites are above the horizon during the search window
+ **TLEFetcher**: downloads TLE files for use in the program
+ **AzimuthFilter**: filters satellites based on whether their azimuth in relation to the facility intersects with the telescope's azimuth
