
from os import sep as osSep

from hasiihelper.ResourceManager import ResourceManager

from pkg_resources import resource_filename

from json import load as jsonLoad

import logging.config


class LocateResources:

    # noinspection SpellCheckingInspection
    RESOURCE_ENV_VAR:             str = 'RESOURCEPATH'
    # noinspection SpellCheckingInspection
    RESOURCES_PACKAGE_NAME:       str = 'pytrek.resources'
    # noinspection SpellCheckingInspection
    FONT_RESOURCES_PACKAGE_NAME:  str = 'pytrek.resources.fonts'
    # noinspection SpellCheckingInspection
    IMAGE_RESOURCES_PACKAGE_NAME: str = 'pytrek.resources.images'
    # noinspection SpellCheckingInspection
    SOUND_RESOURCES_PACKAGE_NAME: str = 'pytrek.resources.sounds'

    # noinspection SpellCheckingInspection
    RESOURCES_PATH:       str = f'pytrek{osSep}resources'
    SOUND_RESOURCES_PATH: str = f'{RESOURCES_PATH}{osSep}sounds'
    IMAGE_RESOURCES_PATH: str = f'{RESOURCES_PATH}{osSep}images'
    FONT_RESOURCES_PATH:  str = f'{RESOURCES_PATH}{osSep}fonts'

    JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"

    PACKAGE_TO_PATH_MAP: dict = {RESOURCES_PACKAGE_NAME:       RESOURCES_PATH,
                                 FONT_RESOURCES_PACKAGE_NAME:  FONT_RESOURCES_PATH,
                                 IMAGE_RESOURCES_PACKAGE_NAME: IMAGE_RESOURCES_PATH,
                                 SOUND_RESOURCES_PACKAGE_NAME: SOUND_RESOURCES_PATH
                                 }

    @staticmethod
    def setupSystemLogging():

        configFilePath: str = ResourceManager.retrieveResourcePath(bareFileName=LocateResources.JSON_LOGGING_CONFIG_FILENAME,
                                                                   resourcePath=LocateResources.RESOURCES_PATH,
                                                                   packageName=LocateResources.RESOURCES_PACKAGE_NAME)
        with open(configFilePath, 'r') as loggingConfigurationFile:
            configurationDictionary = jsonLoad(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads   = False

    # noinspection SpellCheckingInspection
    @staticmethod
    def getResourcesPath(resourcePackageName: str, bareFileName: str) -> str:
        # Use this method in Python 3.9
        # from importlib_resources import files
        # configFilePath: str  = files('pytrek.resources').joinpath(JSON_LOGGING_CONFIG_FILENAME)
        try:
            fqFileName: str = resource_filename(resourcePackageName, bareFileName)
        except (ValueError, Exception):
            #
            # Maybe we are in an app
            #
            from os import environ
            # pathToResources: str = environ.get(LocateResources.RESOURCE_ENV_VAR)
            pathToResources: str = environ[LocateResources.RESOURCE_ENV_VAR]
            resourcesPath:   str = LocateResources.PACKAGE_TO_PATH_MAP[resourcePackageName]
            fqFileName = f'{pathToResources}/{resourcesPath}/{bareFileName}'

        return fqFileName
