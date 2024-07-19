import math
import numpy as np

from typing import List

from sopp.custom_dataclasses.configuration import Configuration
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.custom_dataclasses.satellite.satellite import Satellite

R = 6371.0  # approximate radius of Earth in km
base_alt = 500 # relative average of altitude in km, tbd might need to change or alter value

class CartesianCoordinate:
    def __init__(self, x: float, y: float, z: float):
        self.x = x  # x-coordinate
        self.y = y  # y-coordinate
        self.z = z  # z-coordinate

    def set_coordinates(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_coordinates(self):
        return self.x, self.y, self.z
    
    def pass_to_rotation_matrix(self, gamma: float, phi: float):
        matrixOne = np.array([
            [np.cos(gamma), -np.sin(gamma), 0],
            [np.sin(gamma), np.cos(gamma), 0],
            [0, 0, 1]
        ])

        matrixTwo = np.array([
            [np.cos(phi), 0, np.sin(phi)],
            [0, 1, 0],
            [-np.sin(phi), 0, np.cos(phi)]
        ])
        origMatrix = np.matmul(matrixOne, matrixTwo)
        totMatrix = origMatrix.T
        cartesianArray = np.array([self.x,self.y,self.z])
        return self.apply_rotation(totMatrix,cartesianArray)
    
    def apply_rotation(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
        """
        Apply rotation matrix to a vector of Cartesian coordinates.
    
        Args:
        - matrix (np.ndarray): 3x3 rotation matrix
        - vector (np.ndarray): 1x3 vector of Cartesian coordinates [x, y, z]
    
        Returns:
        - np.ndarray: Resulting vector after rotation
        """
        return np.matmul(matrix, vector)
    
    def cartesian_to_spherical(self) -> List[float]:
        """
        Convert Cartesian coordinates to spherical coordinates.
        """

        x = self.x
        y = self.y
        z = self.z

        r = np.sqrt(x**2 + y**2 + z**2)  # Radial distance

        theta = np.arccos(z/r)

        if x > 0:
            phi = np.arctan(y/x)
        if x < 0 and y >= 0:
            phi = np.arctan(y/x) + np.pi
        if x < 0 and y < 0:
            phi = np.arctan(y/x) - np.pi
        if x == 0 and y > 0:
            phi = np.pi/2
        if x == 0 and y < 0:
            phi = -np.pi/2
        if x == 0 and y == 0:
            phi = 0 # default value because this is undefined, maybe change this to some other value?

        return [theta, phi]



class SatelliteLinkBudgetAngleCalculator:
    def __init__(self, ground_antenna_direction: PositionTime, satellite_position: PositionTime, satellite: Satellite):
        self.ground_antenna_direction = ground_antenna_direction
        self.satellite_position = satellite_position
        self.satellite = satellite

    def get_link_angles(self):
        results = []
        ground_ab = self.calculate_ab_ground()
        sat_ab = self.calculate_ab_sat()
        results.append(ground_ab[0])
        results.append(ground_ab[1])
        results.append(sat_ab[0])
        results.append(sat_ab[1])
        return results  #results are in alpha, beta for each 
    
    def calculate_ab_ground(self) -> List[float]: #calculates the alpha and beta angles for gain pattern of the ground antenna
        satellite_cartesian = self.satellite_position.position.to_cartesian()
        rotated_vector = satellite_cartesian.pass_to_rotation_matrix(self.ground_antenna_direction.position.azimuth, (90-self.ground_antenna_direction.position.altitude))
        x = rotated_vector[0]
        y = rotated_vector[1]
        z = rotated_vector[2]
        new_coordinate = CartesianCoordinate(x,y,z)
        return new_coordinate.cartesian_to_spherical()
    
    def calculate_ab_sat(self) -> List[float]: #calculates the alpha and beta angles for gain pattern of the satellite antenna
        #assuming that we can just invert the cartesian coordinate system, this works in the exact same way as above
        ground_cartesian = self.satellite_position.position.to_cartesian()
        rotated_vector = ground_cartesian.pass_to_rotation_matrix(self.satellite.antenna.direction.azimuth, (90-self.satellite.antenna.direction.altitude))
        x = rotated_vector[0]
        y = rotated_vector[1]
        z = rotated_vector[2]
        new_coordinate = CartesianCoordinate(x,y,z)
        return new_coordinate.cartesian_to_spherical()


    #### some of the functions below this were used before and might become useful for additional algorithms in the future, but are not in use in this file


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

