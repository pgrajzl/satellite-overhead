import os
from dotenv import load_dotenv

load_dotenv()
IDENTITY = os.getenv("IDENTITY")
PASSWORD = os.getenv("PASSWORD")

''' 
Function to download TLEs from Space-Track.org. First authenticates to space-track.org and gets cookie,
then uses curl to download the 3-line elements and save them to a file. Credentials currently hardcoded.
'''
def fetchTLE():
    print("Logging into SPACE-TRACK...")
    os.system(f'curl -c cookies.txt -b cookies.txt https://www.space-track.org/ajaxauth/login -d "identity={IDENTITY}&password={PASSWORD}"')
    print("Fetching TLE...")
    os.system('curl --limit-rate 100K --cookie cookies.txt https://www.space-track.org/basicspacedata/query/class/gp/EPOCH/%3Enow-30/format/3le > ./TLEdata/test.txt')

fetchTLE()

'''
TODO
add check so that TLEs are only fetched if current file is out of date by certain time frame




'''
