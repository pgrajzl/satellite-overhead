from pathlib import Path
from typing import Optional

from sopp.config_file.support.config_file_base import ConfigFileBase
from sopp.config_file.support.config_file_json import ConfigFileJson
from sopp.utilities import get_default_config_file_filepath


def get_config_file_object(config_filepath: Optional[Path] = None) -> ConfigFileBase:
    config_filepath = config_filepath or get_default_config_file_filepath()
    for config_class in [ConfigFileJson]:
        if config_class.filename_extension() in str(config_filepath):
            return config_class(filepath=config_filepath)
