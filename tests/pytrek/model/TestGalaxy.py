
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy

from pytrek.GameState import GameState
from pytrek.model.Quadrant import Quadrant
from pytrek.settings.GameSettings import GameSettings

from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase


class TestGalaxy(TestBase):

    clsLogger:    Logger = cast(Logger, None)
    clsGameSettings: GameSettings = cast(GameSettings, None)
    clsGameState:    GameState    = cast(GameState, None)
    clsGalaxy:       Galaxy       = cast(Galaxy, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGalaxy.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

        TestGalaxy.clsGameSettings = GameSettings()

        TestGalaxy.clsGameSettings.debugCollectKlingonQuadrantCoordinates = True

        TestGalaxy.clsGameState    = GameState()
        TestGalaxy.clsGalaxy       = Galaxy()

    def setUp(self):
        self.logger: Logger = TestGalaxy.clsLogger

        # Set the flag prior to instantiating the Galaxy singleton
        self._gameSettings: GameSettings = TestGalaxy.clsGameSettings

        self._gameState: GameState = TestGalaxy.clsGameState
        self._galaxy:    Galaxy    = TestGalaxy.clsGalaxy

    def tearDown(self):
        self._gameSettings.debugCollectKlingonQuadrantCoordinates = False

    def testPlaceKlingonsInGalaxyCount(self):
        """
        Use the debug list created during initialization
        Assumes that the runtime debug flag 'debug_collect_klingon_quadrant_coordinates' is set to True
        """
        gameState: GameState = GameState()
        expectedKlingonCount: int = gameState.remainingKlingons
        #
        # The number of entries in the debug list is the number if klingons we placed
        placedKlingonCount: int = len(self._galaxy._debugKlingonQuadrants)

        self.assertEqual(expectedKlingonCount, placedKlingonCount, 'Either we placed too little or too many klingons')

    def testPlaceKlingonsInGalaxyPositions(self):
        """
        Use the debug list created during initialization
        Assumes that the runtime debug flag 'debug_collect_klingon_quadrant_coordinates' is set to True
        """
        galaxy: Galaxy = self._galaxy
        debugKlingonQuadrants: List[Coordinates] = galaxy._debugKlingonQuadrants
        for kCoordinates in debugKlingonQuadrants:
            kCoordinates: Coordinates = cast(Coordinates, kCoordinates)
            quadrant: Quadrant = galaxy.getQuadrant(kCoordinates)
            self.assertNotEqual(0, quadrant.klingonCount, 'We should have some Klingons in this quadrant')
            self.logger.debug(f'{kCoordinates=} {quadrant.klingonCount=}')

    def testGetStarBaseCoordinates(self):

        self.assertNotEqual(0, self._gameState.starBaseCount, 'Should always have some StarBases')

        randomCoordinates: Coordinates = self._galaxy.getStarBaseCoordinates()

        self.assertIsNotNone(randomCoordinates, "We should get somebody")

        self.logger.debug(f'{randomCoordinates=}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGalaxy))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
