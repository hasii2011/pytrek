
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.model.Coordinates import Coordinates
from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase


class TestGamePiece(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGamePiece.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger: Logger = TestGamePiece.clsLogger

    def tearDown(self):
        pass

    def testGamePositionToScreenPositionZeroZero(self):

        sectorCoordinates: Coordinates = Coordinates(x=0, y=0)
        arcadePoint:       ArcadePoint = GamePiece.gamePositionToScreenPosition(gameCoordinates=sectorCoordinates)

        self.logger.info(f'{arcadePoint=}')

        expectedPoint: ArcadePoint = ArcadePoint(x=32.0, y=798.0)
        self.assertEqual(expectedPoint, arcadePoint, 'Calculation must have changed')

    def testGamePositionToScreenPositionOneZero(self):

        sectorCoordinates: Coordinates = Coordinates(x=1, y=0)
        arcadePoint:       ArcadePoint = GamePiece.gamePositionToScreenPosition(gameCoordinates=sectorCoordinates)

        self.logger.info(f'{arcadePoint=}')

        expectedPoint: ArcadePoint = ArcadePoint(x=96.0, y=798.0)
        self.assertEqual(expectedPoint, arcadePoint, 'Calculation must have changed')

    def testGamePositionToScreenPositionZeroNine(self):

        sectorCoordinates: Coordinates = Coordinates(x=0, y=9)
        arcadePoint:       ArcadePoint = GamePiece.gamePositionToScreenPosition(gameCoordinates=sectorCoordinates)

        self.logger.info(f'{arcadePoint=}')

        expectedPoint: ArcadePoint = ArcadePoint(x=32.0, y=222.0)
        self.assertEqual(expectedPoint, arcadePoint, 'Calculation must have changed')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGamePiece))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
