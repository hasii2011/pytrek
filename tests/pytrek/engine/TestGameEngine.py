
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from pytrek.engine.GameEngine import GameEngine


class TestGameEngine(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGameEngine.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:      Logger     = TestGameEngine.clsLogger
        self._gameEngine: GameEngine = GameEngine()

    def tearDown(self):
        pass

    def testName1(self):
        pass

    def testName2(self):
        """Another test"""
        pass


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGameEngine))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
