# S.O.P.P. - Satellite Orbit Prediction Processor

## Run

### Setting up the supplemental files

#### Active Satellites TLE File
There should be a [TLE](https://en.wikipedia.org/wiki/Two-line_element_set) file, containing the satellites that you 
want to search through, at `supplements/active_sats.tle` under the root directory.

#### Config file
There should be a file at `supplements/.config` under the root directory to set default values for a reservation. 
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
      - `active_sats.tle`: contents described in section #active-satellites-tle-file.
      - `.config`: contents described in section #config-file section.

```bash
docker run 
  -v "<PATH_TO_LOCAL_SUPPLEMENTAL_DIRECTORY>:/satellite_orbit_prediction/supplements" \
  sopp
```
