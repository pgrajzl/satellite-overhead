import json
from pathlib import Path


def read_json_file(filepath: Path) -> dict:
    with open(filepath, 'r') as f:
        return json.load(f)
