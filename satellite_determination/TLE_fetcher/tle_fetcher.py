import os

import requests
from satellite_determination.utilities import SATELLITES_FILENAME, SUPPLEMENTS_DIRECTORY_NAME, get_satellites_filepath
from dotenv import load_dotenv

'''
TleFetcher will pull tles from either Space-Track or Celestrak. User credentials are required to pull from Space-Track;
see the README for how to set up these credentials in your environment.
'''

load_dotenv()
IDENTITY = os.getenv("IDENTITY")
PASSWORD = os.getenv("PASSWORD")


class TleFetcher():
    def get_tles_spacetrak(self):
        print('Logging into Space-Track...')
        os.system(f'curl -c cookies.txt -b cookies.txt https://www.space-track.org/ajaxauth/login -d "identity={IDENTITY}&password={PASSWORD}"')
        os.system(f'curl --limit-rate 100K --cookie cookies.txt https://www.space-track.org/basicspacedata/query/class/gp/EPOCH/%3Enow-30/format/3le > ./{SUPPLEMENTS_DIRECTORY_NAME}/{SATELLITES_FILENAME}')

    def get_tles_celestrak(self):
        print('Pulling active satellite TLEs from Celestrak...')
        active_sats_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
        tles = requests.get(active_sats_url, allow_redirects=True)
        tle_file_path = get_satellites_filepath()
        tle_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(tle_file_path, 'wb') as f:
            f.write(tles.content)
            f.close()


