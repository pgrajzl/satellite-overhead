from skyfield.api import load, wgs84

'''
Function to load TLE data into the Skyfield EarthSatellite object
EarthSatellites contain the following:
-epoch: the epoch moment for the orbit parameters
-name: sat name
-model.satnum: sat id number

'''

def loadSatellites(sat_tles):
    satellites = load.tle_file(sat_tles)
    print('Loaded', len(satellites), 'satellites')
    return satellites
    #for sat in satellites:
        #print(sat.epoch.utc_jpl())


#TODO: add frequency?
#new object?