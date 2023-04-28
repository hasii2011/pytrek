
from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType
from pytrek.model.Quadrant import Quadrant

from tests.TestBase import TestBase


class TestQuadrant(TestBase):
    """
    """
    def testInitialization(self):

        coordinates: Coordinates = Coordinates(1, 1)
        quadrant:    Quadrant    = Quadrant(coordinates=coordinates)

        self.assertIsNotNone(quadrant, 'Should initialize')

    def testGetRandomEmptySector(self):
        """
        """
        coordinates: Coordinates = Coordinates(1, 1)
        quadrant:    Quadrant = Quadrant(coordinates=coordinates)
        sector:      Sector   = quadrant.getRandomEmptySector()

        self.assertIsNotNone(sector, "Gotta get a sector back")
        self.assertEqual(sector.type, SectorType.EMPTY, "sector should be empty")

        self.logger.info(f'retrieved sector: {sector}')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestQuadrant))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
