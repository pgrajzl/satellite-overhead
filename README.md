# S.O.P.P. - Satellite Orbit Prediction Processor

## Docker
Run the following commands from the root directory

### Build

```bash
docker build . -t sopp
```

### Run
In the following command, your `<PATH_TO_LOCAL_TLE_DATA_DIRECTORY>` directory should contain a file named
`active_sats.txt` that is a [TLE](https://en.wikipedia.org/wiki/Two-line_element_set) file containing the 
satellites that you want to search through. 

```bash
docker run 
  -v "<PATH_TO_LOCAL_TLE_DATA_DIRECTORY>:/cu_pass/TLEData" \
  sopp
```
