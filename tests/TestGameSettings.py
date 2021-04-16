
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.GameSettings import GameSettings
from tests.TestBase import TestBase

# import the class you want to test here
# from pytrek.tests.TestGameSettings import TestGameSettings


class TestGameSettings(TestBase):
    """
    You need to change the name of this class to Test`XXXX`
    Where `XXXX' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGameSettings.clsLogger = getLogger(__name__)
        GameSettings.determineSettingsLocation()

    def setUp(self):
        self.logger: Logger = TestGameSettings.clsLogger
        #
        # TODO: Save the game settings file before running unit tests
        #

    def tearDown(self):
        pass

    def testSettingExistence(self):
        """
        Only tests the existence of settings not their default value
        """

        settings = GameSettings()

        self.assertIsNotNone(settings.maximumStarCount)
        self.assertIsNotNone(settings.maximumStarBase)
        self.assertIsNotNone(settings.minimumStarBase)
        self.assertIsNotNone(settings.maximumPlanets)
        #
        # self.assertIsNotNone(settings.initialEnergyLevel)
        # self.assertIsNotNone(settings.initialShieldEnergy)
        # self.assertIsNotNone(settings.minimumImpulseEnergy)
        #
        # self.assertIsNotNone(settings.gameLengthFactor)
        # self.assertIsNotNone(settings.starBaseExtender)
        # self.assertIsNotNone(settings.starBaseMultiplier)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGameSettings))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
