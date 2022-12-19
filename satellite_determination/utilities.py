import json
from pathlib import Path
from datetime import datetime
import pytz


def read_json_file(filepath: Path) -> dict:
    with open(filepath, 'r') as f:
        return json.load(f)

def convert_tz_to_utc(localtime: str) -> datetime:
    format = "%m/%d/%Y %H:%M:%S"
    local_dt = datetime.strptime(localtime, format)
    dt_utc = local_dt.astimezone(pytz.UTC)
    return dt_utc

def convert_dt_to_utc(localtime: datetime) -> datetime:
    dt_utc = localtime.astimezone(pytz.UTC)
    return dt_utc