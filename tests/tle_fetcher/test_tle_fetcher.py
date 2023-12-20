import pytest
import requests
from pathlib import Path

from sopp.tle_fetcher.tle_fetcher_base import TleFetcherBase
from sopp.tle_fetcher.tle_fetcher_celestrak import TleFetcherCelestrak

class MockRequestResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code
        self.content = 'mock tle data'.encode(encoding='UTF-8')

class StubTleFetcher(TleFetcherBase):
    def __init__(self, tle_file_path: str = None):
        super().__init__(tle_file_path=tle_file_path)

    def _fetch_content(self):
        return requests.get('http://mock/test/url')

class TestTleFetcher:
    def test_fetch_tles_invalid_status(self, monkeypatch, tmp_path):
        fetcher = StubTleFetcher(tle_file_path=str(tmp_path))

        with monkeypatch.context() as m:
            m.setattr(requests, 'get', lambda *args, **kwargs: MockRequestResponse(status_code=404))
            with pytest.raises(requests.exceptions.HTTPError) as _:
                response = fetcher.fetch_tles()

    def test_fetch_tles_request_exception(self, monkeypatch, tmp_path):
        fetcher = StubTleFetcher(tle_file_path=str(tmp_path))

        def raise_exception(args, **kwargs):
            raise requests.exceptions.HTTPError

        with monkeypatch.context() as m:
            m.setattr(requests, 'get', raise_exception)
            with pytest.raises(requests.exceptions.HTTPError) as _:
                response = fetcher.fetch_tles()

    def test_fetch_tles_success(self, monkeypatch, tmp_path):
        tmp_file = tmp_path/'mock'
        fetcher = StubTleFetcher(tle_file_path=str(tmp_file))

        with monkeypatch.context() as m:
            m.setattr(requests, 'get', lambda *args, **kwargs: MockRequestResponse())
            response = fetcher.fetch_tles()

        assert response == Path(fetcher._tle_file_path)
