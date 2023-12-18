
from unittest import TestSuite
from unittest import main as unitTestMain

from tests.ProjectTestBase import ProjectTestBase

from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds


class TestTorpedoSpeeds(ProjectTestBase):
    """
    """

    def testParseSpeedString(self):

        valueStr: str = '10,20,30,40'

        tp: TorpedoSpeeds = TorpedoSpeeds.toTorpedoSpeed(valueStr)

        self.assertEqual(10, tp.enterprise, 'Invalid Enterprise value')
        self.assertEqual(20, tp.klingon,    'Invalid Klingon value')
        self.assertEqual(30, tp.commander,  'Invalid Commander value')
        self.assertEqual(40, tp.superCommander, 'Invalid Super Commander value')

    def testTooManyValues(self):
        valueStr: str = '10,20,30,40,50'
        self.assertRaises(ValueError, lambda: self._raiseException(valueStr=valueStr))

    def testTooFewValues(self):
        valueStr: str = '10,20,30'
        self.assertRaises(ValueError, lambda: self._raiseException(valueStr=valueStr))

    # noinspection PyUnusedLocal
    def _raiseException(self, valueStr: str):
        tp: TorpedoSpeeds = TorpedoSpeeds.toTorpedoSpeed(valueStr)


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestTorpedoSpeeds))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
