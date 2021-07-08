
from typing import cast

from logging import Logger
from logging import getLogger

from math import degrees

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.Constants import MAX_SECTOR_X_COORDINATE
from pytrek.Constants import MAX_SECTOR_Y_COORDINATE
from pytrek.Constants import MIN_SECTOR_X_COORDINATE
from pytrek.Constants import MIN_SECTOR_Y_COORDINATE
from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.KlingonPower import KlingonPower

from pytrek.model.Coordinates import Coordinates

from pytrek.engine.Computer import Computer
from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase


class TestComputer(TestBase):
    """
    Test all of our computer math
    """
    MIN_QUADRANT_DISTANCE               = 0
    MAX_QUADRANT_DIAGONAL_DISTANCE      = 1.2
    MAX_QUADRANT_PERPENDICULAR_DISTANCE = 0.9

    SMALL_QUADRANT_DISTANCE: float = 0.60

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestComputer.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

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

    def testComputeHitValueOnEnterpriseFarAwayEmeritus(self):
        """
        Normally klingon power is computed by the Intelligence engine;  We just need a known value to work against
        """

        klingonCoordinates:    Coordinates = Coordinates(0, 0)
        enterpriseCoordinates: Coordinates = Coordinates(9, 9)
        klingonPower:          float       = KlingonPower.Emeritus.value

        hitValue: float = self.smarty.computeHitValueOnEnterprise(klingonCoordinates, enterpriseCoordinates, klingonPower)
        self.logger.info(f"Emeritus Far away.  Klingon hit value: {hitValue:.3f}")
        self.assertAlmostEqual(13.604, hitValue, 3)

    def testComputeHitValueOnEnterpriseUpCloseEmeritus(self):

        klingonCoordinates:    Coordinates = Coordinates(4, 4)
        enterpriseCoordinates: Coordinates = Coordinates(4, 5)
        klingonPower:          float       = KlingonPower.Emeritus.value

        hitValue: float = self.smarty.computeHitValueOnEnterprise(klingonCoordinates, enterpriseCoordinates, klingonPower)
        self.logger.info(f"Emeritus Up Close.  Klingon hit value: {hitValue}")

        self.assertAlmostEqual(600.0, hitValue, 3)

    def testComputeHitValueOnEnterpriseFarAwayNovice(self):

        klingonCoordinates:    Coordinates = Coordinates(0, 0)
        enterpriseCoordinates: Coordinates = Coordinates(9, 9)
        klingonPower:          float       = KlingonPower.Novice.value

        hitValue: float = self.smarty.computeHitValueOnEnterprise(klingonCoordinates, enterpriseCoordinates, klingonPower)
        self.logger.info(f"Novice Far away.  Klingon hit value: {hitValue}")
        self.assertAlmostEqual(10.88, hitValue, 2)

    def testComputeHitValueOnEnterpriseUpCloseNovice(self):

        klingonCoordinates:    Coordinates = Coordinates(4, 5)
        enterpriseCoordinates: Coordinates = Coordinates(4, 4)
        klingonPower:          float       = KlingonPower.Novice.value

        hitValue: float = self.smarty.computeHitValueOnEnterprise(klingonCoordinates, enterpriseCoordinates, klingonPower)
        self.logger.info(f"Novice Up Close.  Klingon hit value: {hitValue}")
        self.assertAlmostEqual(480.0, hitValue, 3)

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

    def testComputeCourseDiagonal(self):

        start: Coordinates = Coordinates(x=0, y=0)
        end:   Coordinates = Coordinates(x=9, y=9)

        course: float = self.smarty._computeCourse(start=start, end=end)
        angle:  float = degrees(course)
        self.assertEqual(45, angle, 'Busted code')
        self.logger.info(f'{course=} {angle=}')

    def testComputeCourseBackDiagonal(self):

        start: Coordinates = Coordinates(x=0, y=0)
        end:   Coordinates = Coordinates(x=9, y=9)

        backwardCourse: float = self.smarty._computeCourse(start=end, end=start)
        backAngle:      float = degrees(backwardCourse)
        self.assertEqual(-135, backAngle, 'Who changed my code')

        self.logger.info(f'{backwardCourse=}, {backAngle=}')

    def testComputeCourseStraightEast(self):

        start: Coordinates = Coordinates(x=0, y=5)
        end:   Coordinates = Coordinates(x=9, y=5)

        course: float = self.smarty._computeCourse(start=start, end=end)
        angle:  float = degrees(course)
        self.assertEqual(0, angle, 'Did calculation chang')
        self.logger.info(f'{course=} {angle=}')

    def testComputeCourseStraightWest(self):

        end:   Coordinates = Coordinates(x=0, y=5)
        start: Coordinates = Coordinates(x=9, y=5)

        course: float = self.smarty._computeCourse(start=start, end=end)
        angle:  float = degrees(course)
        self.assertEqual(180, angle, 'Did calculation chang')
        self.logger.info(f'{course=} {angle=}')

    def testComputeCourseDown(self):

        start: Coordinates = Coordinates(x=0, y=0)
        end:   Coordinates = Coordinates(x=0, y=9)

        course:    float = self.smarty._computeCourse(start=start, end=end)
        downAngle: float = degrees(course)

        self.assertEqual(90, downAngle, 'Hmm, messed up code')
        self.logger.info(f'{course=} {downAngle=}')

    def testComputeCourseUp(self):

        start: Coordinates = Coordinates(x=0, y=0)
        end:   Coordinates = Coordinates(x=0, y=9)

        backwardCourse: float = self.smarty._computeCourse(start=end, end=start)
        backAngle:      float = degrees(backwardCourse)
        self.assertEqual(-90, backAngle, 'Who changed my code')
        self.logger.info(f'{backwardCourse=} {backAngle=}')

    def testComputeHitValueOnKlingon(self):

        testKlingonPower: float = 480.0

        enterprisePosition: Coordinates = Coordinates(x=0, y=0)
        klingonPosition:   Coordinates = Coordinates(x=0, y=9)

        for x in range(10):
            kHit: float = self.smarty.computeHitValueOnKlingon(enterprisePosition=enterprisePosition,
                                                               klingonPosition=klingonPosition,
                                                               klingonPower=testKlingonPower)

            self.logger.info(f'Iteration: {x} - kHit={kHit:.2f}')

            if kHit <= testKlingonPower:
                self.assertLess(kHit, testKlingonPower, 'Single torpedo can almost never kill a Klingon')
            else:
                self.logger.info(f'Iteration: {x} killed a Klingon')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestComputer))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
