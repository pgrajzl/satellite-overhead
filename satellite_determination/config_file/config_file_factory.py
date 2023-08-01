from pathlib import Path
from typing import Optional

from satellite_determination.config_file.support.config_file_base import ConfigFileBase
from satellite_determination.config_file.support.config_file_json import ConfigFileJson
from satellite_determination.config_file.support.config_file_standard import ConfigFileStandard
from satellite_determination.utilities import get_default_config_file_filepath


def get_config_file_object(config_filepath: Optional[Path] = None) -> ConfigFileBase:
    config_filepath = config_filepath or get_default_config_file_filepath()
    for config_class in (ConfigFileStandard, ConfigFileJson):
        if config_class.filename_extension() in str(config_filepath):
            return config_class(filepath=config_filepath)
