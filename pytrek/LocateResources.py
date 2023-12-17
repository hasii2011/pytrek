
from os import sep as osSep

from codeallybasic.ResourceManager import ResourceManager

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

    @classmethod
    def setupSystemLogging(cls):

        configFilePath: str = ResourceManager.retrieveResourcePath(bareFileName=LocateResources.JSON_LOGGING_CONFIG_FILENAME,
                                                                   resourcePath=LocateResources.RESOURCES_PATH,
                                                                   packageName=LocateResources.RESOURCES_PACKAGE_NAME)
        with open(configFilePath, 'r') as loggingConfigurationFile:
            configurationDictionary = jsonLoad(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads   = False

    @classmethod
    def getResourcesPath(cls, bareFileName: str, resourcePath: str, packageName: str) -> str:

        fqFileName: str = ResourceManager.retrieveResourcePath(bareFileName=bareFileName, resourcePath=resourcePath, packageName=packageName)

        return fqFileName

    @classmethod
    def getImagePath(cls, bareFileName: str) -> str:
        fqFileName: str = cls.getResourcesPath(bareFileName=bareFileName,
                                               resourcePath=cls.IMAGE_RESOURCES_PATH,
                                               packageName=cls.IMAGE_RESOURCES_PACKAGE_NAME)
        return fqFileName
