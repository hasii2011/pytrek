
from logging import Logger
from logging import getLogger

from os import environ as osEnvironment
from os import sep as osSep
from pathlib import Path

HOME_ENV_VAR:            str = 'HOME'
XDG_CONFIG_HOME_ENV_VAR: str = 'XDG_CONFIG_HOME'
# defines the base directory relative to which user specific configuration files should be stored.

CONFIGURATION_DIRECTORY: str = '.config'


class ConfigurationLocator:
    """

    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        try:
            self._configurationHome: Path = Path(osEnvironment[XDG_CONFIG_HOME_ENV_VAR])
        except KeyError:
            try:
                homeDir:  str           = osEnvironment[HOME_ENV_VAR]
                self._configurationHome = Path(f'{homeDir}/{CONFIGURATION_DIRECTORY}')
            except KeyError:
                self._configurationHome = Path.cwd()
        finally:
            if Path(self._configurationHome).exists() is False:
                self._configurationHome.mkdir(parents=True)

    @property
    def configurationHome(self) -> Path:
        return Path(self._configurationHome)
