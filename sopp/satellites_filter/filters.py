from typing import Callable

from sopp.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from sopp.custom_dataclasses.satellite.satellite import Satellite


def filter_frequency(observation_frequency: FrequencyRange) -> Callable[[Satellite], bool]:
    """
    filter_frequency returns True if a satellite's downlink transmission frequency
    overlaps with the desired observation frequency. If there is no information
    on the satellite frequency, it will return True to err on the side of caution
    for potential interference.

    Parameters:
    - observation_frequency: An object representing the desired observation frequency.

    Returns:
    - A lambda function that takes a Satellite object and returns True if the conditions
      for frequency filtering are met, False otherwise.
    """
    if observation_frequency:
        return lambda satellite: (
            not satellite.frequency
            or any(sf.frequency is None for sf in satellite.frequency)
            or any(
                sf.status != 'inactive' and observation_frequency.overlaps(sf)
                for sf in satellite.frequency
            )
        )
    else:
        return lambda satellite: True

def filter_name_contains(substring: str) -> Callable[[Satellite], bool]:
    """
    filter_name_contains returns a lambda function that checks if a given substring
    is present in the name of a Satellite.

    Parameters:
    - substring: The substring to check for in the satellite names.

    Returns:
    - A lambda function that takes a Satellite object and returns True if the name
      contains the specified substring, False otherwise.
    """
    return lambda satellite: not substring or substring in satellite.name

def filter_name_does_not_contain(substring: str) -> Callable[[Satellite], bool]:
    """
    filter_name_does_not_contain returns a lambda function that checks if a given substring
    is not present in the name of a Satellite.

    Parameters:
    - substring: The substring to check for absence in the satellite names.

    Returns:
    - A lambda function that takes a Satellite object and returns True if the name
      does not contain the specified substring, False otherwise.
    """
    return lambda satellite: not substring or not filter_name_contains(substring)(satellite)

def filter_name_is(substring: str) -> Callable[[Satellite], bool]:
    """
    filter_name_is returns a lambda function that checks if a given substring
    matches exactly the name of a Satellite.

    Parameters:
    - substring: The substring to match exactly in the satellite names.

    Returns:
    - A lambda function that takes a Satellite object and returns True if the name
      matches the specified substring exactly, False otherwise.
    """
    return lambda satellite: not substring or substring == satellite.name

def filter_orbit_is(orbit_type: str) -> Callable[[Satellite], bool]:
    """
    filter_orbit_type returns a lambda function to filter satellites based on their orbital type.

    Parameters:
    - orbit_type (str): The type of orbit ('leo', 'meo', or 'geo').

    Returns:
    - A lambda function that takes a Satellite object and returns True if it is in the specified orbit type, False otherwise.
    """
    if orbit_type == 'leo':
        return lambda satellite: satellite.orbits_per_day >= 5.0
    elif orbit_type == 'meo':
        return lambda satellite: satellite.orbits_per_day >= 1.5 and satellite.orbits_per_day < 5.0
    elif orbit_type == 'geo':
        return lambda satellite: satellite.orbits_per_day >= 0.85 and satellite.orbits_per_day < 1.5
    elif not orbit_type:
        return lambda satellite: True
    else:
        raise ValueError("Invalid orbit type. Provide 'leo', 'meo', or 'geo'.")
