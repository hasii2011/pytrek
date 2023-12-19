
from os import environ as osEnvironment
from pathlib import Path

from unittest import TestSuite
from unittest import main as unitTestMain


from pytrek.settings.SettingsCommon import SettingsCommon

from tests.ProjectTestBase import ProjectTestBase

from pytrek.ConfigurationLocator import XDG_CONFIG_HOME_ENV_VAR
from pytrek.ConfigurationLocator import HOME_ENV_VAR
from pytrek.ConfigurationLocator import CONFIGURATION_DIRECTORY
from pytrek.ConfigurationLocator import ConfigurationLocator


class TestConfigurationLocator(ProjectTestBase):
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

    def testPlaceInCurrentDirectory(self):
        try:
            del osEnvironment[HOME_ENV_VAR]
        except KeyError:
            pass    # May or may not exist;  don't care
        try:
            del osEnvironment[XDG_CONFIG_HOME_ENV_VAR]
        except KeyError:
            pass    # May or may not exist;  don't care

        configurationLocator: ConfigurationLocator = ConfigurationLocator()
        cwdPath: Path = Path(Path.cwd())

        self.assertEqual(cwdPath, configurationLocator.configurationHome, 'Configuration home should be current directory')

    def testPlaceInHomeDirectory(self):
        try:
            del osEnvironment[XDG_CONFIG_HOME_ENV_VAR]
        except KeyError:
            pass    # May or may not exist;  don't care

        fakeHomePath: Path = Path(f'/tmp/fakeHome/')

        osEnvironment[HOME_ENV_VAR] = fakeHomePath.as_posix()

        fakeConfigurationPath: Path = Path(f'/tmp/fakeHome/{CONFIGURATION_DIRECTORY}')

        configurationLocator: ConfigurationLocator = ConfigurationLocator()

        self.assertEqual(fakeConfigurationPath, configurationLocator.configurationHome, 'Configuration home should be a fake home directory')

    def testPlaceInXDG(self):
        fakeXDGPATH: Path = Path('/tmp/fakeXDG/.config')

        osEnvironment[XDG_CONFIG_HOME_ENV_VAR] = fakeXDGPATH.as_posix()

        configurationLocator: ConfigurationLocator = ConfigurationLocator()

        self.assertEqual(fakeXDGPATH, configurationLocator.configurationHome, 'Configuration home should be a fake home directory')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestConfigurationLocator))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
