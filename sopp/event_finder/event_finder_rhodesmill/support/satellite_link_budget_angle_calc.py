import math

from sopp.custom_dataclasses.configuration import Configuration
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.custom_dataclasses.satellite.satellite import Satellite

R = 6371.0  # approximate radius of Earth in km
base_alt = 500 # relative average of altitude in km, tbd might need to change or alter value

class SatelliteLinkBudgetAngleCalculator:
    def __init__(self, ground_antenna_direction: PositionTime, satellite_position: PositionTime, satellite: Satellite):
        self.ground_antenna_direction = ground_antenna_direction
        self.satellite_position = satellite_position
        self.satellite = satellite

    def get_link_angles(self):
        results = []
        results.append(self.calculate_altitude_difference_ground)
        results.append(self.calculate_azimuth_difference_ground)
        results.append(self.calculate_altitude_difference_space)
        results.append(self.calculate_azimuth_difference_space)
        return results  #results are in alt, az for home antenna first and then alt, az for satellite antenna


    def calculate_azimuth_difference_ground(self): #between antenna direction and direction to satellite
       
        satellite_azimuth = self.satellite_position.position.azimuth
        ground_azimuth = self.ground_antenna_direction.position.altitude

        azimuth_difference = satellite_azimuth - ground_azimuth

        return azimuth_difference

    def calculate_altitude_difference_ground(self): #between antenna direction and direction to satellite
        
        satellite_altitude = self.satellite_position.position.altitude
        ground_altitude = self.ground_antenna_direction.position.altitude

        altitude_difference = satellite_altitude - ground_altitude #sign is going to be important here so we are not calculating absolute value

        return altitude_difference

    def calculate_altitude_difference_space(self): #between satellite pointing direction and direction to ground antenna
        R = 6371.0  # approximate radius of Earth in km
        base_alt = 500 # relative average of altitude in km, tbd might need to change or alter value

        satellite_altitude = self.satellite_position.position.altitude
        satellite_pointing_altitude = self.satellite.antenna.direction.altitude

        # altitude_difference = satellite_altitude - satellite_pointing_altitude #sign is going to be important here so we are not calculating absolute value

        dist = self.satellite_position.position.distance_km
    
        return self.law_of_cosines_angle_c(dist, (R + base_alt), R)
    
    def calculate_azimuth_difference_space(self): #between satellite pointing direction and direction to ground antenna
        R = 6371.0  # approximate radius of Earth in km
        base_alt = 500 # relative average of altitude in km, tbd might need to change or alter value

        satellite_azimuth = self.satellite_position.position.azimuth
        satellite_pointing_azimuth = self.satellite.antenna.direction.azimuth
        pointing_complement = (360 - satellite_pointing_azimuth)

        to_ret = pointing_complement - satellite_azimuth

        return to_ret

    def law_of_cosines_angle_c(a, b, c):
        # Ensure sides are positive (valid triangle sides)
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Side lengths must be positive.")

        # Calculate cos(C) using the law of cosines
        cos_C = (a**2 + b**2 - c**2) / (2 * a * b)

        # Check for valid cosine value range
        if cos_C < -1 or cos_C > 1:
            raise ValueError("Invalid triangle sides - no such triangle exists.")

        # Calculate angle C in radians
        angle_C_rad = math.acos(cos_C)

        # Convert angle from radians to degrees
        angle_C_deg = math.degrees(angle_C_rad)

        return angle_C_deg
        

# Example usage:
if __name__ == "__main__":
    # Example input parameters
    ground_antenna_direction = (120.0, 45.0)  # azimuth and elevation angles in degrees
    satellite_position = (35.0, 140.0, 35786.0)  # latitude, longitude, and altitude in degrees and meters
    satellite_pointing_position = (200.0, 30.0)  # azimuth and elevation angles in degrees

    # Create an instance of the calculator
    calculator = SatelliteLinkBudgetAngleCalculator(ground_antenna_direction, satellite_position, satellite_pointing_position)

    # Calculate the link budget
    link_budget = calculator.calculate_link_budget()

    print(f"Link Budget: {link_budget:.2f} dB")

