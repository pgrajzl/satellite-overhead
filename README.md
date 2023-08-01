# S.O.P.P. - Satellite Orbit Prediction Processor

SOPP is an open-source tool for calculating satellite interference to radio astronomy observations.

![alt text](https://github.com/NSF-Swift/satellite-overhead/blob/main/FBD.png)

## Running SOPP

### Install the requirements:
```bash
>> pip3 install -r requirements.txt
```

### Setting up the supplemental files

The TLE and frequency data is stored in the `supplements` directory.

#### Active Satellites TLE File
There should be a [TLE](https://en.wikipedia.org/wiki/Two-line_element_set) file, containing the satellites that you 
want to search through, at `supplements/satellites.tle` under the root directory. In the SOPP program itself, a list of active satellites are pulled from
Celestrak. If you want to provide it your own TLE file, you can comment out this line and place your own TLE file in the `supplements` directory.

##### Instructions for pulling files from Space-Track
If you want to pull TLE files from Space-Track.org, there are a few extra steps you need to take since the site requires user credentials:

First go to [Space-Track.org](https://www.space-track.org) and register for a user account. 
After you have done this, create a .env file in your root directory:

```bash
>> touch .env
```

Then edit this file using your preferred text editor to contain the following information:

    IDENTITY=<Space-Track.org username>
    PASSWORD=<Space-Track.org password>

where the identity value is the Space-Track username you just registered with and the password value is your password. You should now be able to use the
get_tles_spacetrack() function to pull TLE files.

#### Formatting Frequency File

To use the FrequencyFilter, a frequency CSV file needs to be supplied at `supplements/satellite_frequencies.csv`
The frequency file should consist of the following columns:

|   ID   |   Name   |   Frequency   |   Bandwidth   |   Status   |   Description   |

Where the `ID` is the satellite's NORAD SATCAT ID, the `Name` is the satellite's name, the `Frequency` is the satellite's downlink 
center frequency (in MHz), `Bandwidth` is the bandwidth of the downlink frequency, `Status` is if the antenna is active or not (optional), and 
`Description` contains any antenna characteristics (optional). A satellite frequency scraper is available
[here](https://github.com/NSF-Swift/sat-frequency-scraper) that can be used to generate this file.

#### Config file
There should be a file at `supplements/config.json` under the root directory to set default observation values for a reservation. 
The following is an example of a config file:

    {
      "reservation": {
        "latitude": 40.8178049,
        "longitude": -121.4695413,
        "beamwidth": 3,
        "name": "ARBITRARY_2",
        "startTimeUtc": "2023-03-30T10:00:00.000000",
        "endTimeUtc": "2023-03-30T11:00:00.000000",
        "frequency": 135,
        "bandwidth": 10
      },
      "observationTarget": {
        "declination": "-38d6m50.8s",
        "rightAscension": "4h42m"
      },
    }


Below is a description of each of these values:
+ "latitude" is the latitude of the RA facility
+ "longitude" is the longitude of the RA facility
+ "beamwidth" is the beamwidth of the RA telescope
+ "name" is the name of the RA facility
+ "startTimeUtc" is the desired start time of the observation in UTC
+ "endTimeUtc" is the desired end time of the observation in UTC
+ "frequency" is the center frequency of the observation
+ "bandwidth" is the bandwidth of the desired observation


+ "declination" is the declination value of the celestial target the RA telescope is trying to observe
  + More information can be found in [Astropy's Astronomical Coordinate System](https://docs.astropy.org/en/stable/coordinates/index.html)
+ "rightAscension" is the right ascension value of the celestial target the RA telescope is trying to observe
  + More information can be found in [Astropy's Astronomical Coordinate System](https://docs.astropy.org/en/stable/coordinates/index.html)


###### Static Antenna Position
A static antenna position may be given instead of an observation target's declination and right ascension.
The following is an example config file portion. If both a static antenna position and an observation target is given,
the static antenna position will take precedence.
    
    {
        ...
        "staticAntennaPosition": {
          "altitude": 0.2,
          "azimuth": 0.3
        }
    }


##### Alternate Config File Format
You may alternatively supply the config file in `.config` format at `supplements/.config`. An example is as follows

    [RESERVATION]
    Latitude=40.8178049
    Longitude=-121.4695413
    Beamwidth=3
    Name=HCRO
    StartTimeUTC=2023-03-30T10:00:00.000000
    EndTimeUTC=2023-03-30T15:00:00.000000
    Frequency=135
    Bandwidth=10
    
    [OBSERVATION TARGET]
    Declination=-38d6m50.8s
    Right Ascension=4h42m

    [STATIC ANTENNA POSITION]
    Altitude=0.2
    Azimuth=0.3


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

## Downloading TLE Files Using TLEFetcher

The TLEFetcher can be used to download files from either Space-Track or Celestrak. In the SOPP program itself, a list of active satellites are pulled from
Celestrak. If you want to provide it your own TLE file, you can comment out

## SOPP Components
### Third-Party Tools
- **Space-Track:** [Space-Track.org](https://www.space-track.org) is a site maintained by the U.S. Space Force that allows users to query a database and download satellite TLEs. SOPP contains the functionality to pull satellite TLEs from Space-Track for use in the program, but the site requires users to have an account.
- **Celestrak:** [Celestrak](https://celestrak.org) is the precursor to space-track and is available without an account. While it has been predicted to be phased out for years, it is still actively maintained. It also has an easily downloadable list of active satellites, which doesn’t include space debris.
- **Astropy:** [Astropy](https://www.astropy.org/) is a Python package designed for use in astronomy and contains functions for many space math problems. Astropy is used in the SOPP tool to calculate the path of an observation target through the sky to determine the telescope’s movement as a function of time. These azimuth and elevation values are then used to determine if a satellite’s movement intersects with this path.
- **Rhodesmill Skyfield:** The [Skyfield API](https://rhodesmill.org/skyfield/) is a comprehensive Python package for computing the positions of stars, planets, and satellites. SOPP uses the Skyfield API to find all the satellites visible above the horizon during an observation search window.
- **Satellite Frequencies:** a satellite frequency database was created by scraping frequency information from various open sources. The code used to generated the database can be found [here](https://github.com/NSF-Swift/sat-frequency-scraper).
