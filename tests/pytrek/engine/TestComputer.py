from math import degrees
from math import floor

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.Constants import MAX_QUADRANT_X_COORDINATE
from pytrek.Constants import MAX_QUADRANT_Y_COORDINATE
from pytrek.Constants import MAX_SECTOR_X_COORDINATE
from pytrek.Constants import MAX_SECTOR_Y_COORDINATE
from pytrek.Constants import MIN_QUADRANT_X_COORDINATE
from pytrek.Constants import MIN_SECTOR_X_COORDINATE
from pytrek.Constants import MIN_SECTOR_Y_COORDINATE
from pytrek.Constants import QUADRANT_GRID_WIDTH
from pytrek.Constants import SCREEN_HEIGHT

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer

from pytrek.model.Coordinates import Coordinates


from tests.ProjectTestBase import ProjectTestBase


class TestComputer(ProjectTestBase):
    """
    Test all of our computer math
    """
    MIN_QUADRANT_DISTANCE               = 0
    MAX_QUADRANT_DIAGONAL_DISTANCE      = 1.2
    MAX_QUADRANT_PERPENDICULAR_DISTANCE = 0.9

    SMALL_QUADRANT_DISTANCE: float = 0.60

    MIN_GALACTIC_DISTANCE: float = 0.0
    MAX_GALACTIC_DISTANCE: float = 90.0

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self.smarty: Computer = Computer()

    def testComputerDirectionDown(self):

        startCoordinates: Coordinates = Coordinates(x=5, y=0)
        endCoordinates:   Coordinates = Coordinates(x=5, y=5)

        radianDirection: float = self.smarty.computeGameTravelDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        degreeDirection = degrees(radianDirection)

        self.assertEqual(0.0, degreeDirection, 'Invalid direction')

    def testComputerDirectionLeftToRightAngle(self):

        startCoordinates: Coordinates = Coordinates(x=0, y=0)
        endCoordinates:   Coordinates = Coordinates(x=5, y=5)

        radianDirection: float = self.smarty.computeGameTravelDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        degreeDirection = degrees(radianDirection)

        self.assertAlmostEqual(85.94, degreeDirection, 2, 'Incorrect left to right direction')

    def testComputerDirectionUp(self):

        startCoordinates: Coordinates = Coordinates(x=5, y=5)
        endCoordinates:   Coordinates = Coordinates(x=5, y=0)

        radianDirection: float = self.smarty.computeGameTravelDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        degreeDirection = degrees(radianDirection)

        self.assertAlmostEqual(343.77, degreeDirection, 2, 'Incorrect left to right direction')

    def testComputerDirectionRightToLeftAngle(self):

        startCoordinates: Coordinates = Coordinates(x=5, y=5)
        endCoordinates:   Coordinates = Coordinates(x=0, y=0)

        radianDirection: float = self.smarty.computeGameTravelDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        degreeDirection = degrees(radianDirection)

        self.assertAlmostEqual(-257.83, degreeDirection, 2, 'Incorrect left to right direction')

    def testComputeDestinationCoordinates(self):

        startCoordinates: Coordinates = Coordinates(x=5, y=5)

        destinationCoordinates: Coordinates = self.smarty.computeDestinationCoordinates(startCoordinates=startCoordinates, distance=0.5, angle=6.0)

        expectedCoordinates: Coordinates = Coordinates(x=5, y=5)

        self.assertEqual(expectedCoordinates, destinationCoordinates, 'Computer is broken')

    def testKnownCoordinates_2_1(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=163, y=775)
        expectedCoordinates: Coordinates = Coordinates(x=2, y=1)

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Computer is broken')

    def testKnownCoordinates_4_9(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=293, y=272)
        expectedCoordinates: Coordinates = Coordinates(x=4, y=9)

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Computer is broken')

    def testKnownCoordinates_8_9(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=553, y=272)
        expectedCoordinates: Coordinates = Coordinates(x=8, y=9)

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Computer is broken')

    def testKnownCoordinates_8_3(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=553, y=650)
        expectedCoordinates: Coordinates = Coordinates(x=8, y=3)

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

    def testComputeGalacticDistanceWestToEast(self):
        """
        Not going to retest distance computations between inter-quadrant and galactic travel
        as galactic is just 10 times more expensive
        """

        startQuadrantCoordinates = Coordinates(MAX_QUADRANT_X_COORDINATE, floor(MAX_QUADRANT_Y_COORDINATE // 2))
        endQuadrantCoordinates   = Coordinates(MIN_QUADRANT_X_COORDINATE, floor(MAX_QUADRANT_Y_COORDINATE // 2))

        self.logger.info(f"West to East quadrant coordinates {startQuadrantCoordinates}, {endQuadrantCoordinates}")

        distance = self.smarty.computeGalacticDistance(startQuadrantCoordinates=startQuadrantCoordinates, endQuadrantCoordinates=endQuadrantCoordinates)
        self.logger.info(f"Galactic West/East distance is: {distance}")

        self.assertGreater(distance, TestComputer.MIN_GALACTIC_DISTANCE, "East/West calculation failed less than zero")
        self.assertEqual(distance,   TestComputer.MAX_GALACTIC_DISTANCE, "Incorrect West/East distance")

    def testComputeGalacticDistanceModerateUp(self):

        startCoordinates = Coordinates(x=5, y=5)
        endCoordinates   = Coordinates(x=5, y=0)

        distance       = self.smarty.computeGalacticDistance(startQuadrantCoordinates=startCoordinates, endQuadrantCoordinates=endCoordinates)
        # sectorDistance = self.smarty.computeQuadrantDistance(startSector=startCoordinates, endSector=endCoordinates)

        self.assertEqual(distance, 50.0, "Incorrect West/East distance")

    def testValueStringEmptyQuadrant(self):

        strValue = self.smarty.createValueString(klingonCount=0, commanderCount=0, hasStarBase=False)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("000", strValue, "Empty quadrant is all zeroes")

    def testValueStringMultiKlingon(self):

        strValue = self.smarty.createValueString(klingonCount=3, commanderCount=0, hasStarBase=False)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("300", strValue, "Must contain 3 Klingons and no StarBase")

    def testValueStringMultiKlingonAndStarBase(self):

        strValue = self.smarty.createValueString(klingonCount=4, commanderCount=0, hasStarBase=True)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("410", strValue, "Must contain 4 Klingons and a StarBase")

    def testValueStringMultiKlingonCommanderAndStarBase(self):

        strValue = self.smarty.createValueString(klingonCount=4, commanderCount=1, hasStarBase=True)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("510", strValue, "Must contain 4 Klingons and a StarBase")

    def testValueStringMultiKlingonCommanderAndNoStarBase(self):

        strValue = self.smarty.createValueString(klingonCount=4, commanderCount=1, hasStarBase=False)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("500", strValue, "Must contain 4 Klingons and a StarBase")

    def testGalaxyArcadePosition_212_786(self):

        expectedArcade: ArcadePoint = ArcadePoint(x=212, y=786)
        actualArcade:   ArcadePoint = Computer.gamePositionToScreenPoint(gameCoordinates=Coordinates(x=3, y=0))

        self.assertEqual(expectedArcade, actualArcade, 'Computer is broken')

    def testGalaxyArcadePosition_20_594(self):

        expectedArcade: ArcadePoint = ArcadePoint(x=20, y=594)
        actualArcade:   ArcadePoint = Computer.gamePositionToScreenPoint(gameCoordinates=Coordinates(x=0, y=3))

        self.assertEqual(expectedArcade, actualArcade, 'Computer is broken')

    def testGalaxyArcadePosition_276_530(self):

        expectedArcade: ArcadePoint = ArcadePoint(x=276, y=530)
        actualArcade:   ArcadePoint = Computer.gamePositionToScreenPoint(gameCoordinates=Coordinates(x=4, y=4))

        self.assertEqual(expectedArcade, actualArcade, 'Computer is broken')

    def testGalaxyArcadePosition_84_786(self):

        expectedArcade: ArcadePoint = ArcadePoint(x=84, y=786)
        actualArcade:   ArcadePoint = Computer.gamePositionToScreenPoint(gameCoordinates=Coordinates(x=1, y=0))

        self.assertEqual(expectedArcade, actualArcade, 'Computer is broken')

    def testGalaxyArcadePosition_596_201(self):

        expectedArcade: ArcadePoint = ArcadePoint(x=596, y=210)
        actualArcade:   ArcadePoint = Computer.gamePositionToScreenPoint(gameCoordinates=Coordinates(x=9, y=9))

        self.assertEqual(expectedArcade, actualArcade, 'Computer is broken')

    def testComputeAngleToTargetDirectNorth(self):
        """
        North is up
        """

        shooter:  ArcadePoint = ArcadePoint(x=100, y=100)
        deadMeat: ArcadePoint = ArcadePoint(x=100, y=500)

        actualAngle = self.smarty.computeAngleToTarget(shooter=shooter, deadMeat=deadMeat)
        expectedAngle = 90

        self.assertEqual(expectedAngle, actualAngle, 'Bad computation')

    def testComputeAngleToTargetDirectSouth(self):
        """
        South is down
        """

        shooter:  ArcadePoint = ArcadePoint(x=100.0, y=500.0)
        deadMeat: ArcadePoint = ArcadePoint(x=100.0, y=100.0)

        actualAngle:   float = self.smarty.computeAngleToTarget(shooter=shooter, deadMeat=deadMeat)
        expectedAngle: float = -90.0

        self.assertEqual(expectedAngle, actualAngle, 'Bad computation')

    def testComputeAngleToTargetDirectEast(self):
        """
        East is right
        """

        shooter:  ArcadePoint = ArcadePoint(x=100.0, y=100.0)
        deadMeat: ArcadePoint = ArcadePoint(x=500.0, y=100.0)

        actualAngle:   float = self.smarty.computeAngleToTarget(shooter=shooter, deadMeat=deadMeat)
        expectedAngle: float = 0.0

        self.assertEqual(expectedAngle, actualAngle, 'Bad computation')

    def testComputeAngleToTargetDirectWest(self):
        """
        East is right
        """

        shooter:  ArcadePoint = ArcadePoint(x=500.0, y=100.0)
        deadMeat: ArcadePoint = ArcadePoint(x=100.0, y=100.0)

        actualAngle:   float = self.smarty.computeAngleToTarget(shooter=shooter, deadMeat=deadMeat)
        expectedAngle: float = 180.0

        self.assertEqual(expectedAngle, actualAngle, 'Bad computation')

    def testComputeCenterPointLong(self):

        startPoint: ArcadePoint = ArcadePoint(x=10, y=10)
        endPoint:   ArcadePoint = ArcadePoint(x=SCREEN_HEIGHT-10, y=QUADRANT_GRID_WIDTH-10)

        midPoint: ArcadePoint = Computer.computeCenterPoint(start=startPoint, end=endPoint)

        self.logger.debug(f'{startPoint=} {endPoint=} {midPoint=}')

        expectedPoint: ArcadePoint = ArcadePoint(x=435, y=320)
        self.assertEqual(expectedPoint, midPoint, 'Long Center point does not match')

    def testComputeCenterPointShort(self):

        startPoint: ArcadePoint = ArcadePoint(x=400, y=400)
        endPoint:   ArcadePoint = ArcadePoint(x=600, y=600)

        midPoint: ArcadePoint = Computer.computeCenterPoint(start=startPoint, end=endPoint)

        self.logger.debug(f'{startPoint=} {endPoint=} {midPoint=}')

        expectedPoint: ArcadePoint = ArcadePoint(x=500, y=500)
        self.assertEqual(expectedPoint, midPoint, 'Short Center point does not match')

    def testComputeCenterPointMid(self):

        startPoint: ArcadePoint = ArcadePoint(x=0, y=0)
        endPoint:   ArcadePoint = ArcadePoint(x=400, y=400)

        midPoint: ArcadePoint = Computer.computeCenterPoint(start=startPoint, end=endPoint)

        self.logger.debug(f'{startPoint=} {endPoint=} {midPoint=}')

        expectedPoint: ArcadePoint = ArcadePoint(x=200, y=200)
        self.assertEqual(expectedPoint, midPoint, 'Mid Center point does not match')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestComputer))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
