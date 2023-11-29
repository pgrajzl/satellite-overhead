import os

import requests
from sopp.utilities import SATELLITES_FILENAME, SUPPLEMENTS_DIRECTORY_NAME, get_satellites_filepath
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
        spacetrack_url = 'https://www.space-track.org/ajaxauth/login'
        query = 'https://www.space-track.org/basicspacedata/query/class/gp/decay_date/null-val/epoch/%3Enow-30/orderby/norad_cat_id/format/3le'
        data = {'identity': IDENTITY, 'password': PASSWORD, 'query': query}
        tles = requests.post(url=spacetrack_url, data=data)
        self._write_tles_to_file(tles.content)

    def get_tles_celestrak(self):
        print('Pulling active satellite TLEs from Celestrak...')
        active_sats_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
        tles = requests.get(active_sats_url, allow_redirects=True)
        self._write_tles_to_file(tles.content)

    def _write_tles_to_file(self, content):
        tle_file_path = get_satellites_filepath()
        tle_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(tle_file_path, 'wb') as f:
            f.write(content)
            f.close()
