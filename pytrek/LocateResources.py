
from os import sep as osSep

from pkg_resources import resource_filename


class LocateResources:

    RESOURCE_ENV_VAR:             str = 'RESOURCEPATH'
    RESOURCES_PACKAGE_NAME:       str = 'pytrek.resources'
    FONT_RESOURCES_PACKAGE_NAME:  str = 'pytrek.resources.fonts'
    IMAGE_RESOURCES_PACKAGE_NAME: str = 'pytrek.resources.images'
    SOUND_RESOURCES_PACKAGE_NAME: str = 'pytrek.resources.sounds'

    RESOURCES_PATH:       str = f'pytrek{osSep}resources'
    SOUND_RESOURCES_PATH: str = f'{RESOURCES_PATH}{osSep}sounds'
    IMAGE_RESOURCES_PATH: str = f'{RESOURCES_PATH}{osSep}images'
    FONT_RESOURCES_PATH:  str = f'{RESOURCES_PATH}{osSep}fonts'

    JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"

    @staticmethod
    def getResourcesPath(resourcePackageName: str, resourcesPath: str, bareFileName: str) -> str:
        # Use this method in Python 3.9
        # from importlib_resources import files
        # configFilePath: str  = files('org.hasii.pytrek.resources').joinpath(JSON_LOGGING_CONFIG_FILENAME)
        try:
            fqFileName: str = resource_filename(resourcePackageName, bareFileName)
        except (ValueError, Exception):
            #
            # Maybe we are in an app
            #
            from os import environ
            pathToResources: str = environ.get(f'{LocateResources.RESOURCE_ENV_VAR}')
            fqFileName:      str = f'{pathToResources}/{resourcesPath}/{bareFileName}'

        return fqFileName
