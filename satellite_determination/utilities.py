import json
import os
from contextlib import contextmanager
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path
from typing import ContextManager, Optional
from uuid import uuid4

import pytz


def read_json_file(filepath: Path) -> dict:
    with open(filepath, 'r') as f:
        return json.load(f)


@contextmanager
def temporary_file(filepath: Optional[Path] = None) -> ContextManager[TextIOWrapper]:
    filepath = Path(filepath or f'{uuid4().hex}.tmp')
    with open(filepath, 'w') as f:
        yield f
    filepath.unlink(missing_ok=True)

def convert_datetime_to_utc(localtime: datetime) -> datetime:
    if localtime.tzinfo == pytz.UTC:
        return localtime
    elif localtime.tzinfo is None:
        dt_utc = localtime.replace(tzinfo=pytz.UTC)
        return dt_utc
    else:
        dt_utc = localtime.astimezone(pytz.UTC)
        return dt_utc

def get_script_directory(module) -> Path:
    return Path(os.path.dirname(os.path.realpath(module)))

def get_root_directory(module) -> Path:
    return Path(os.path.dirname(os.path.abspath(__file__)))
