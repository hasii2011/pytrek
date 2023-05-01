
from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.model.Coordinates import Coordinates

from tests.TestBase import TestBase


class TestGamePiece(TestBase):
    """
    """

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
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGamePiece))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
