from dataclasses import dataclass

from sgp4.exporter import export_tle
from sgp4.model import Satrec
from sgp4.vallado_cpp import WGS72

from satellite_determination.custom_dataclasses.satellite.international_designator import InternationalDesignator
from satellite_determination.custom_dataclasses.satellite.mean_motion import MeanMotion


@dataclass
class TleInformation:
    argument_of_perigee: float
    drag_coefficient: float
    eccentricity: float
    epoch_days: float
    inclination: float
    international_designator: InternationalDesignator
    mean_anomaly: float
    mean_motion: MeanMotion
    revolution_number: int
    right_ascension_of_ascending_node: float
    satellite_number: int
    classification: str = 'U'

    def __str__(self):
        satrec = Satrec()
        satrec.sgp4init(
            WGS72,
            'i',
            self.satellite_number,
            self.epoch_days,
            self.drag_coefficient,
            self.mean_motion.first_derivative,
            self.mean_motion.second_derivative,
            self.eccentricity,
            self.argument_of_perigee,
            self.inclination,
            self.mean_anomaly,
            self.mean_motion.value,
            self.right_ascension_of_ascending_node,
        )
        satrec.classification = self.classification
        satrec.intldesg = str(self.international_designator)
        satrec.revnum = self.revolution_number
        tle_lines = export_tle(satrec=satrec)
        return '\n'.join(tle_lines)
