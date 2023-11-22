from sopp.path_finder.observation_path_finder_astropy import ObservationPathFinderAstropy
from path_finder_base_test import PathFinderBaseTest


class TestPathFinderAstropy(PathFinderBaseTest):
    PathFinderClass = ObservationPathFinderAstropy
