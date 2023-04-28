
from typing import cast

import logging
import logging.config

import json

from unittest import TestCase

from pkg_resources import resource_filename

from hasiihelper.Singleton import Singleton

from pytrek.GameState import GameState

from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.futures.EventEngine import EventEngine
from pytrek.mediators.GalaxyMediator import GalaxyMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

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
        GameSettings.__instance__ = cast(Singleton, None)
        Intelligence.__instance__ = cast(Singleton, None)
        GameState.__instance__    = cast(Singleton, None)
        Galaxy.__instance__       = cast(Singleton, None)
        GameEngine.__instance__   = cast(Singleton, None)
        EventEngine.__instance__  = cast(Singleton, None)
        Devices.__instance__      = cast(Singleton, None)
        Galaxy.__instance__       = cast(Singleton, None)
        GalaxyMediator.__instance__   = cast(Singleton, None)
        QuadrantMediator.__instance__ = cast(Singleton, None)

