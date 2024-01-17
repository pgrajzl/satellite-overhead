def frequency_filter(observation_frequency):
    """
    frequency_filter returns True if a satellite's downlink transmission frequency
    overlaps with the desired observation frequency. If there is no information
    on the satellite frequency, it will return True to err on the side of caution
    for potential interference.

    Parameters:
    - observation_frequency: An object representing the desired observation frequency.

    Returns:
    - A lambda function that takes a Satellite object and returns True if the conditions
      for frequency filtering are met, False otherwise.
    """
    return lambda sat: (
        not sat.frequency or any(sf.frequency is None for sf in sat.frequency)
    ) or (
        any(
            sf.status != 'inactive' and observation_frequency.overlaps(sf)
            for sf in sat.frequency
        )
    )

def name_contains_filter(substring):
    """
    name_contains_filter returns a lambda function that checks if a given substring
    is present in the name of a Satellite.

    Parameters:
    - substring: The substring to check for in the satellite names.

    Returns:
    - A lambda function that takes a Satellite object and returns True if the name
      contains the specified substring, False otherwise.
    """
    return lambda sat: substring in sat.name

def not_name_contains_filter(substring):
    """
    not_name_contains_filter returns a lambda function that checks if a given substring
    is not present in the name of a Satellite.

    Parameters:
    - substring: The substring to check for absence in the satellite names.

    Returns:
    - A lambda function that takes a Satellite object and returns True if the name
      does not contain the specified substring, False otherwise.
    """
    return lambda sat: substring not in sat.name

def name_is_filter(substring):
    """
    name_is_filter returns a lambda function that checks if a given substring
    matches exactly the name of a Satellite.

    Parameters:
    - substring: The substring to match exactly in the satellite names.

    Returns:
    - A lambda function that takes a Satellite object and returns True if the name
      matches the specified substring exactly, False otherwise.
    """
    return lambda sat: substring == sat.name

def leo_filter():
    """
    leo_filter returns a lambda function to filter Low Earth Orbit (LEO) satellites based on their orbital period.

    The filter checks if the satellite's orbital period is less than or equal to 128.0 minutes.

    Returns:
    - A lambda function that takes a Satellite object and returns True if it is in LEO, False otherwise.
    """
    return lambda sat: sat.orbital_period <= 128.0

def meo_filter():
    """
    meo_filter returns a lambda function to filter Medium Earth Orbit (MEO) satellites based on their orbital period.

    The filter checks if the satellite's orbital period is greater than 128.0 and less than 1430.0 minutes.

    Returns:
    - A lambda function that takes a Satellite object and returns True if it is in MEO, False otherwise.
    """
    return lambda sat: sat.orbital_period > 128.0 and sat.orbital_period < 1430.0

def geo_filter():
    """
    geo_filter returns a lambda function to filter Geostationary Orbit (GEO) satellites based on their orbital period.

    The filter checks if the absolute difference between the satellite's orbital period and 1436.0 minutes
    is less than or equal to 1.0 minute, providing a tolerance for geostationary orbital periods.

    Returns:
    - A lambda function that takes a Satellite object and returns True if it is in GEO, False otherwise.
    """
    return lambda sat: abs(sat.orbital_period - 1436.0) <= 1.0
