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
    return lambda satellite: (
        not satellite.frequency or any(sf.frequency is None for sf in satellite.frequency)
    ) or (
        any(
            sf.status != 'inactive' and observation_frequency.overlaps(sf)
            for sf in satellite.frequency
        )
    )

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
    return lambda satellite: substring in satellite.name

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
    return lambda satellite: substring not in satellite.name

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
    return lambda satellite: substring == satellite.name

def filter_is_leo() -> Callable[[Satellite], bool]:
    """
    filter_is_leo returns a lambda function to filter Low Earth Orbit (LEO) satellites based on their orbital period.

    The filter checks if the satellite's orbits per day is >= 5.0

    Returns:
    - A lambda function that takes a Satellite object and returns True if it is in LEO, False otherwise.
    """
    return lambda satellite: satellite.orbits_per_day >= 5.0

def filter_is_meo() -> Callable[[Satellite], bool]:
    """
    filter_is_meo returns a lambda function to filter Medium Earth Orbit (MEO) satellites based on their orbital period.

    The filter checks if the satellite's orbits per day is >= 1.5 and < 5.0

    Returns:
    - A lambda function that takes a Satellite object and returns True if it is in MEO, False otherwise.
    """
    return lambda satellite: satellite.orbits_per_day >= 1.5 and satellite.orbits_per_day < 5.0

def filter_is_geo() -> Callable[[Satellite], bool]:
    """
    filter_is_geo returns a lambda function to filter Geostationary Orbit (GEO) satellites based on their orbital period.

    The filter checks if the satellite's orbits per day is >= 0.85 and < 1.5

    Returns:
    - A lambda function that takes a Satellite object and returns True if it is in GEO, False otherwise.
    """
    return lambda satellite: satellite.orbits_per_day >= 0.85 and satellite.orbits_per_day < 1.5
