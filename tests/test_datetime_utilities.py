import pytz
from datetime import datetime

from sopp.utilities import read_datetime_string_as_utc


class TestDatetimeUtilities:
    def test_read_datetime_string_as_utc_with_microseconds(self):
        expected_datetime = datetime(2023, 12, 27, 19, 0, 0, 0, tzinfo=pytz.UTC)

        assert read_datetime_string_as_utc('2023-12-27T19:00:00.0') == expected_datetime

    def test_read_datetime_string_as_utc_without_microseconds(self):
        expected_datetime = datetime(2023, 12, 27, 19, 0, 0, 0, tzinfo=pytz.UTC)

        assert read_datetime_string_as_utc('2023-12-27T19:00:00') == expected_datetime

    def test_read_datetime_string_as_utc_with_timezone(self):
        expected_datetime = datetime(2023, 12, 27, 12, 0, 0, 0, tzinfo=pytz.UTC)

        assert read_datetime_string_as_utc('2023-12-27T5:00:00-07:00') == expected_datetime
