
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.model.Coordinates import Coordinates

from pytrek.engine.Computer import Computer

from tests.TestBase import TestBase


class TestComputer(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestComputer.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger   = TestComputer.clsLogger
        self.smarty: Computer = Computer()

    def tearDown(self):
        pass

    def testKnown1(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=163, y=775)
        expectedCoordinates: Coordinates = Coordinates(x=2, y=0)

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Computer is broken')

    def testKnown2(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=293, y=272)
        expectedCoordinates: Coordinates = Coordinates(x=4, y=8)

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Computer is broken')

    def testKnown3(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=553, y=272)
        expectedCoordinates: Coordinates = Coordinates(x=8, y=8)

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Computer is broken')

    def testKnown4(self):

        actualCoordinates:   Coordinates = self.smarty.computeSectorCoordinates(x=553, y=650)
        expectedCoordinates: Coordinates = Coordinates(x=8, y=2)

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Computer is broken')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestTemplate))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
