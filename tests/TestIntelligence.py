
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.Intelligence import Intelligence

from pytrek.model.Coordinates import Coordinates

from tests.TestBase import TestBase


class TestIntelligence(TestBase):

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestIntelligence.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestIntelligence.clsLogger

        self.smarty: Intelligence = Intelligence()

    def testGetRandomSectorCoordinates(self):
        """"""
        coordinates = self.smarty.generateSectorCoordinates()
        self.assertIsNotNone(coordinates, "Should not be null")
        self.logger.info("random coordinates: '%s'", coordinates)

        bogusCoordinate = Coordinates(-1, -1)

        self.assertNotEqual(coordinates, bogusCoordinate, "Not truly initializing random coordinates")


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutVisibilityEnum))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
