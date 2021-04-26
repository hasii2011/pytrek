
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.Direction import Direction
from pytrek.model.Coordinates import Coordinates
from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase

STANDARD_X_COORDINATE: int = 4
STANDARD_Y_COORDINATE: int = 4

EXPECTED_Y_COORDINATE_MOVEMENT_NORTH: int = 3
EXPECTED_Y_COORDINATE_MOVEMENT_SOUTH: int = 5
EXPECTED_X_COORDINATE_MOVEMENT_EAST: int  = 5
EXPECTED_X_COORDINATE_MOVEMENT_WEST: int  = 3

EXPECTED_X_COORDINATE_NE_MOVEMENT: int = 5
EXPECTED_Y_COORDINATE_NE_MOVEMENT: int = 3
EXPECTED_X_COORDINATE_NW_MOVEMENT: int = 3
EXPECTED_Y_COORDINATE_NW_MOVEMENT: int = 3
EXPECTED_X_COORDINATE_SW_MOVEMENT: int = 3
EXPECTED_Y_COORDINATE_SW_MOVEMENT: int = 5

EXPECTED_X_COORDINATE_SE_MOVEMENT: int = 5
EXPECTED_Y_COORDINATE_SE_MOVEMENT: int = 5


class TestCoordinates(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestCoordinates.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

    def setUp(self):
        self.logger: Logger = TestCoordinates.clsLogger

    def tearDown(self):
        pass

    def testNewCoordinatesNorth(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.North)

        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_MOVEMENT_NORTH, "Should have decremented 'y'")

    def testNewCoordinatesSouth(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.South)

        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_MOVEMENT_SOUTH, "Should have incremented 'y'")

    def testNewCoordinatesEast(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.East)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_MOVEMENT_EAST, "Should have incremented 'x'")

    def testNewCoordinatesWest(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.West)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_MOVEMENT_WEST, "Should have decremented 'x'")

    def testNewCoordinatesNorthEast(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.NorthEast)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_NE_MOVEMENT, "Should have incremented 'x'")
        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_NE_MOVEMENT, "Should have decremented 'y'")

    def testNewCoordinatesNorthWest(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.NorthWest)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_NW_MOVEMENT, "Should have decremented 'x'")
        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_NW_MOVEMENT, "Should have decremented 'y'")

    def testNewCoordinatesSouthWest(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.SouthWest)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_SW_MOVEMENT, "Should have decremented 'x'")
        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_SW_MOVEMENT, "Should have incremented 'y'")

    def testNewCoordinatesSouthEast(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.SouthEast)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_SE_MOVEMENT, "Should have incremented 'x'")
        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_SE_MOVEMENT, "Should have incremented 'y'")

    def testXTooSmall(self):
        coordinate = Coordinates(-1, 0)
        self.assertFalse(coordinate.valid())

    def testXTooBig(self):
        coordinate = Coordinates(10, 0)
        self.assertFalse(coordinate.valid())

    def testXLowBoundaryOk(self):
        coordinate = Coordinates(0, 0)
        self.assertTrue(coordinate.valid())

    def testXMidValueOk(self):
        coordinate = Coordinates(5, 0)
        self.assertTrue(coordinate.valid())

    def testXHighBoundaryOk(self):
        coordinate = Coordinates(9, 0)
        self.assertTrue(coordinate.valid())

    def testYTooSmall(self):
        coordinate = Coordinates(0, -1)
        self.assertFalse(coordinate.valid())

    def testYTooBig(self):
        coordinate = Coordinates(0, 10)
        self.assertFalse(coordinate.valid())

    def testYLowBoundaryOk(self):
        coordinate = Coordinates(0, 0)
        self.assertTrue(coordinate.valid())

    def testYMidValueOk(self):
        coordinate = Coordinates(0, 5)
        self.assertTrue(coordinate.valid())

    def testYHighBoundaryOk(self):
        coordinate = Coordinates(0, 9)
        self.assertTrue(coordinate.valid())


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestCoordinates))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
