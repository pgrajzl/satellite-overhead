import requests

from sopp.tle_fetcher.tle_fetcher_base import TleFetcherBase


class TleFetcherCelestrak(TleFetcherBase):
    def __init__(self, tle_file_path: str = None):
        super().__init__(tle_file_path=tle_file_path)

    def _fetch_content(self):
        url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'

        return requests.get(url=url, allow_redirects=True)
