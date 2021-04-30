
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.Constants import MAX_SECTOR_X_COORDINATE
from pytrek.Constants import MAX_SECTOR_Y_COORDINATE
from pytrek.Constants import MIN_SECTOR_X_COORDINATE
from pytrek.Constants import MIN_SECTOR_Y_COORDINATE

from pytrek.model.Coordinates import Coordinates

from pytrek.engine.Computer import Computer

from tests.TestBase import TestBase


class TestComputer(TestBase):
    """
    Test all of our computer math
    """
    MIN_QUADRANT_DISTANCE               = 0
    MAX_QUADRANT_DIAGONAL_DISTANCE      = 1.2
    MAX_QUADRANT_PERPENDICULAR_DISTANCE = 0.9

    SMALL_QUADRANT_DISTANCE: float = 0.60

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestComputer.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger   = TestComputer.clsLogger
        self.smarty: Computer = Computer()

    def tearDown(self):
        pass

    def testKnownCoordinates_2_0(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=163, y=775)
        expectedCoordinates: Coordinates = Coordinates(x=2, y=0)

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Computer is broken')

    def testKnownCoordinates_4_8(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=293, y=272)
        expectedCoordinates: Coordinates = Coordinates(x=4, y=8)

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Computer is broken')

    def testKnownCoordinates_8_8(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=553, y=272)
        expectedCoordinates: Coordinates = Coordinates(x=8, y=8)

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Computer is broken')

    def testKnownCoordinates_8_2(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=553, y=650)
        expectedCoordinates: Coordinates = Coordinates(x=8, y=2)

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Computer is broken')

    def testComputeQuadrantDistanceTopLeftToBottomRight(self):
        """
        """

        startSectorCoordinates = Coordinates(MIN_SECTOR_X_COORDINATE, MIN_SECTOR_Y_COORDINATE)
        endSectorCoordinates   = Coordinates(MAX_SECTOR_X_COORDINATE, MAX_SECTOR_Y_COORDINATE)

        distance: float = self.smarty.computeQuadrantDistance(startSector=startSectorCoordinates, endSector=endSectorCoordinates)

        self.logger.info(f"Max distance is: {distance}")
        self.assertGreater(distance, TestComputer.MIN_QUADRANT_DISTANCE, "Max distance calculation failed less than zero")
        self.assertGreaterEqual(distance, TestComputer.MAX_QUADRANT_DIAGONAL_DISTANCE, "Incorrect max distance")

    def testComputeQuadrantDistanceBottomRightToTopLeft(self):
        """
        """
        startSectorCoordinates = Coordinates(MAX_SECTOR_X_COORDINATE, MAX_SECTOR_Y_COORDINATE)
        endSectorCoordinates   = Coordinates(MIN_SECTOR_X_COORDINATE, MIN_SECTOR_Y_COORDINATE)

        distance = self.smarty.computeQuadrantDistance(startSector=startSectorCoordinates, endSector=endSectorCoordinates)

        self.logger.info(f"Reverse Max distance is: {distance}")
        self.assertGreater(distance, TestComputer.MIN_QUADRANT_DISTANCE, "Max distance calculation failed less than zero")
        self.assertGreaterEqual(distance, TestComputer.MAX_QUADRANT_DIAGONAL_DISTANCE, "Incorrect reverse max distance")

    def testComputeQuadrantDistanceEastToWest(self):
        """"""

        startSectorCoordinates = Coordinates(MIN_SECTOR_X_COORDINATE, MAX_SECTOR_Y_COORDINATE // 2)
        endSectorCoordinates   = Coordinates(MAX_SECTOR_X_COORDINATE, MAX_SECTOR_Y_COORDINATE // 2)

        self.logger.info(f"East to West coordinates {startSectorCoordinates}, {endSectorCoordinates} ")

        distance = self.smarty.computeQuadrantDistance(startSector=startSectorCoordinates, endSector=endSectorCoordinates)

        self.logger.info(f"East/West distance is: {distance}")
        self.assertGreater(distance, TestComputer.MIN_QUADRANT_DISTANCE, "East/West calculation failed less than zero")
        self.assertEqual(distance, TestComputer.MAX_QUADRANT_PERPENDICULAR_DISTANCE, "Incorrect East/West distance")

    def testComputeQuadrantDistanceWestToEast(self):
        """"""
        startSectorCoordinates = Coordinates(MAX_SECTOR_X_COORDINATE, MAX_SECTOR_Y_COORDINATE // 2)
        endSectorCoordinates   = Coordinates(MIN_SECTOR_X_COORDINATE, MAX_SECTOR_Y_COORDINATE // 2)

        self.logger.info("Quadrant West to East sector coordinates %s, %s ", startSectorCoordinates, endSectorCoordinates)

        distance = self.smarty.computeQuadrantDistance(startSector=startSectorCoordinates, endSector=endSectorCoordinates)
        self.logger.info("West/East distance is: %s", distance)
        self.assertGreater(distance, TestComputer.MIN_QUADRANT_DISTANCE, "East/West calculation failed less than zero")
        self.assertEqual(distance, TestComputer.MAX_QUADRANT_PERPENDICULAR_DISTANCE, "Incorrect East/West distance")

    def testComputeQuadrantDistanceSmall(self):

        startSectorCoordinates = Coordinates(4, 2)
        endSectorCoordinates   = Coordinates(4, 8)

        self.logger.info(f"Small distance sector coordinates {startSectorCoordinates}, {endSectorCoordinates}")
        distance = self.smarty.computeQuadrantDistance(startSector=startSectorCoordinates, endSector=endSectorCoordinates)
        self.logger.info(f"West/East distance is: {distance}")

    def testValueStringEmptyQuadrant(self):

        strValue = self.smarty.createValueString(klingonCount=0, commanderCount=0, hasStarBase=False)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("000", strValue, "Empty quadrant is all zeroes")

    def testValueStringMultiKlingon(self):

        strValue = self.smarty.createValueString(klingonCount=3, commanderCount=0, hasStarBase=False)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("300", strValue, "Must contain 3 Klingons and no starbase")

    def testValueStringMultiKlingonAndStarbase(self):

        strValue = self.smarty.createValueString(klingonCount=4, commanderCount=0, hasStarBase=True)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("410", strValue, "Must contain 4 Klingons and a starbase")

    def testValueStringMultiKlingonCommanderAndStarbase(self):

        strValue = self.smarty.createValueString(klingonCount=4, commanderCount=1, hasStarBase=True)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("510", strValue, "Must contain 4 Klingons and a starbase")

    def testValueStringMultiKlingonCommanderAndNoStarbase(self):

        strValue = self.smarty.createValueString(klingonCount=4, commanderCount=1, hasStarBase=False)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("500", strValue, "Must contain 4 Klingons and a starbase")


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestComputer))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
