
import json

import logging
import logging.config

from unittest import TestCase

from pkg_resources import resource_filename

from pytrek.GameState import GameState

from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.futures.EventEngine import EventEngine

from pytrek.model.Galaxy import Galaxy

from pytrek.settings.GameSettings import GameSettings

JSON_LOGGING_CONFIG_FILENAME: str = "testLoggingConfiguration.json"
TEST_DIRECTORY:               str = 'tests'


class TestBase(TestCase):

    RESOURCES_PACKAGE_NAME:              str = 'tests.resources'
    RESOURCES_TEST_CLASSES_PACKAGE_NAME: str = 'tests.resources.testclass'

    """
    A base unit test class to initialize some logging stuff we need
    """
    @classmethod
    def setUpLogging(cls):
        """
        """
        loggingConfigFilename: str = cls.findLoggingConfig()

        with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def findLoggingConfig(cls) -> str:

        fqFileName = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

        return fqFileName

    @classmethod
    def resetSingletons(cls):
        """
        Force stateful singletons to re-initialize
        """
        GameSettings.__instance__ = None
        Intelligence.__instance__ = None
        GameState.__instance__    = None
        Galaxy.__instance__       = None
        GameEngine.__instance__   = None
        EventEngine.__instance__  = None
        Devices.__instance__      = None
        Galaxy.__instance__       = None
