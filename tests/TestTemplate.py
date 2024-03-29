
from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.settings.SettingsCommon import SettingsCommon

from tests.ProjectTestBase import ProjectTestBase

# import the class you want to test here
# from pytrek.tests.TestTemplate import TestTemplate


class TestTemplate(ProjectTestBase):
    """
    You need to change the name of this class to Test`XXXX`
    Where `XXXX` is the name of the class that you want to test.

    See existing tests for more information.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        SettingsCommon.determineSettingsLocation()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testName1(self):
        pass

    def testName2(self):
        """Another test"""
        pass


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestTemplate))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
