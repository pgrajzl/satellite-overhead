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

    def to_tle_lines(self):
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
        satrec.intldesg = self.international_designator.to_tle_string()
        satrec.revnum = self.revolution_number
        return export_tle(satrec=satrec)

    @classmethod
    def from_tle_lines(cls, line1: str, line2: str) -> 'TleInformation':
        satrec = Satrec.twoline2rv(line1=line1, line2=line2)
        return TleInformation(
            argument_of_perigee=satrec.argpo,
            drag_coefficient=satrec.bstar,
            eccentricity=satrec.ecco,
            epoch_days=satrec.jdsatepoch - 2433281.5 + satrec.jdsatepochF,
            inclination=satrec.inclo,
            international_designator=InternationalDesignator.from_tle_string(satrec.intldesg),
            mean_anomaly=satrec.mo,
            mean_motion=MeanMotion(
                first_derivative=satrec.ndot,
                second_derivative=satrec.nddot,
                value=satrec.no_kozai
            ),
            revolution_number=satrec.revnum,
            right_ascension_of_ascending_node=satrec.nodeo,
            satellite_number=satrec.satnum,
            classification=satrec.classification
        )
