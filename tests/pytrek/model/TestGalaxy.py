
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy

from pytrek.GameState import GameState
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase


class TestGalaxy(TestBase):

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGalaxy.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

    def setUp(self):
        self.logger: Logger = TestGalaxy.clsLogger

        self._galaxy: Galaxy = Galaxy()

    def tearDown(self):
        pass

    def testPlaceKlingonsInGalaxyCount(self):
        """
        Use the debug list created during initialization
        Assumes the the unit test logging configuration has
        pytrek.model.Galaxy   set to DEBUG;  Other the debug list is not created
        """
        gameState: GameState = GameState()
        expectedKlingonCount: int = gameState.remainingKlingons
        #
        # The number of entries in the debug list is the number if klingons we placed
        placedKlingonCount: int = len(self._galaxy._debugKlingonQuadrants)

        self.assertEqual(expectedKlingonCount, placedKlingonCount, 'Either we placed to little or too many klingons')

    def testPlaceKlingonsInGalaxyPositions(self):
        """
        Use the debug list created during initialization
        Assumes the the unit test logging configuration has
        pytrek.model.Galaxy   set to DEBUG;  Other the debug list is not created
        """
        galaxy: Galaxy = self._galaxy
        debugKlingonQuadrants: List[Coordinates] = galaxy._debugKlingonQuadrants
        for kCoordinates in debugKlingonQuadrants:
            kCoordinates: Coordinates = cast(Coordinates, kCoordinates)
            quadrant: Quadrant = galaxy.getQuadrant(kCoordinates)
            self.assertNotEqual(0, quadrant.klingonCount)
            self.logger.warning(f'{kCoordinates=} {quadrant.klingonCount=}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGalaxy))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
