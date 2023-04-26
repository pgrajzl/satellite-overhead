# S.O.P.P. - Satellite Orbit Prediction Processor

## Docker
Run the following commands from the root directory

### Build

```bash
docker build . -t sopp
```

### Run

```bash
docker run 
  -v "<PATH_TO_LOCAL_TLE_DATA_DIRECTORY>:/cu_pass/TLEData" \
  sopp
```
