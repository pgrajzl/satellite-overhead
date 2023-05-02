import os
from dotenv import load_dotenv

load_dotenv()
IDENTITY = os.getenv("IDENTITY")
PASSWORD = os.getenv("PASSWORD")
class TleFetcher():
    def get_tles(self):
        print('Logging into Space-Track...')
        os.system(f'curl -c cookies.txt -b cookies.txt https://www.space-track.org/ajaxauth/login -d "identity={IDENTITY}&password={PASSWORD}"')
        os.system('curl --limit-rate 100K --cookie cookies.txt https://www.space-track.org/basicspacedata/query/class/gp/EPOCH/%3Enow-30/format/3le > ./TLEdata/test.txt')

TleFetcher().get_tles()
