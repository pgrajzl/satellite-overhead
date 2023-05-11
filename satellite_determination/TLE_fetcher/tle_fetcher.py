import os

import requests
from utilities import get_root_directory
from dotenv import load_dotenv

load_dotenv()
IDENTITY = os.getenv("IDENTITY")
PASSWORD = os.getenv("PASSWORD")
class TleFetcher():
    def get_tles_spacetrak(self):
        print('Logging into Space-Track...')
        os.system(f'curl -c cookies.txt -b cookies.txt https://www.space-track.org/ajaxauth/login -d "identity={IDENTITY}&password={PASSWORD}"')
        os.system('curl --limit-rate 100K --cookie cookies.txt https://www.space-track.org/basicspacedata/query/class/gp/EPOCH/%3Enow-30/format/3le > ./supplements/satellites.tle')

    def get_tles_celestrak(self):
        print('Pulling active satellite TLEs from Celestrak...')
        active_sats_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
        tles = requests.get(active_sats_url, allow_redirects=True)
        tle_file_path = str(get_root_directory(__file__)) + '/supplements/' + 'satellites.tle'
        f = open(tle_file_path, 'wb')
        f.write(tles.content)
        f.close()


