import os
from pathlib import Path


def get_script_directory(module) -> Path:
    return Path(os.path.dirname(os.path.realpath(module)))
