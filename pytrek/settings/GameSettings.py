from typing import Dict
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from sys import platform as sysPlatform

from os import getenv as osGetEnv
from os import sep as osSep

from configparser import ConfigParser

from pytrek.Constants import GAME_SETTINGS_FILE_NAME
from pytrek.Constants import THE_GREAT_MAC_PLATFORM
from pytrek.Singleton import Singleton
from pytrek.exceptions.GameSettingsLocationNotSet import GameSettingsLocationNotSet


SettingsNameValues = NewType('SettingsNameValues', Dict[str, str])


class GameSettings(Singleton):

    LIMITS_SECTION: str = 'Limits'

    MAXIMUM_STAR_COUNT: str = 'maximum_star_count'
    MINIMUM_STAR_BASE:  str = 'minimum_star_base'
    MAXIMUM_STAR_BASE:  str = 'maximum_star_base'
    MAXIMUM_PLANETS:    str = 'maximum_planets'

    LIMITS_SETTINGS:  SettingsNameValues = {
        MAXIMUM_STAR_COUNT: '4',
        MINIMUM_STAR_BASE:  '2',
        MAXIMUM_STAR_BASE:  '5',
        MAXIMUM_PLANETS:    '5'
    }

    settingsFileLocationAndName: str = None

    def init(self):

        self.logger: Logger = getLogger(__name__)

        self._config: ConfigParser = cast(ConfigParser, None)    # initialized when empty preferences created

        self._createEmptySettings()
        self._loadSettings()

    @classmethod
    def determineSettingsLocation(cls):
        """
        This method MUST (I repeat MUST) be called before attempting to instantiate the game settings Singleton
        """
        if sysPlatform == "linux2" or sysPlatform == "linux" or sysPlatform == THE_GREAT_MAC_PLATFORM:
            GameSettings.settingsFileLocationAndName = f'{osGetEnv("HOME")}{osSep}{GAME_SETTINGS_FILE_NAME}'
        else:
            GameSettings.settingsFileLocationAndName = GAME_SETTINGS_FILE_NAME

    @classmethod
    def getSettingsLocation(cls):
        if GameSettings.settingsFileLocationAndName is None:
            raise GameSettingsLocationNotSet()
        else:
            return GameSettings.settingsFileLocationAndName

    @property
    def maximumStarCount(self) -> int:
        return self._config.getint(GameSettings.LIMITS_SECTION, GameSettings.MAXIMUM_STAR_COUNT)

    @property
    def minimumStarBase(self) -> int:
        return self._config.getint(GameSettings.LIMITS_SECTION, GameSettings.MINIMUM_STAR_BASE)

    @property
    def maximumStarBase(self) -> int:
        return self._config.getint(GameSettings.LIMITS_SECTION, GameSettings.MAXIMUM_STAR_BASE)

    @property
    def maximumPlanets(self) -> int:
        return self._config.getint(GameSettings.LIMITS_SECTION, GameSettings.MAXIMUM_PLANETS)

    def _createEmptySettings(self):
        self._config: ConfigParser = ConfigParser()

    def _loadSettings(self):
        """
        Load settings from settings file
        """
        # Make sure that the settings file exists
        # noinspection PyUnusedLocal
        try:
            f = open(GameSettings.getSettingsLocation(), "r")
            f.close()
        except (ValueError, Exception) as e:
            try:
                f = open(GameSettings.getSettingsLocation(), "w")
                f.write("")
                f.close()
                self.logger.warning(f'Game Settings File file re-created')
            except (ValueError, Exception) as e:
                self.logger.error(f"Error: {e}")
                return

        self._addMissingLimitsSettings()

    def _addMissingLimitsSettings(self):
        try:
            if self._config.has_section(GameSettings.LIMITS_SECTION) is False:
                self._config.add_section(GameSettings.LIMITS_SECTION)

            for settingName in GameSettings.LIMITS_SETTINGS.keys():
                if self._config.has_option(GameSettings.LIMITS_SECTION, settingName) is False:
                    self._addMissingSetting(GameSettings.LIMITS_SECTION, settingName, GameSettings.LIMITS_SETTINGS[settingName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    def _addMissingSetting(self, sectionName: str, settingName: str, value: str):
        self._config.set(sectionName, settingName, value)
        self._saveConfig()

    def _saveConfig(self):
        """
        Save data to the settings file
        """
        f = open(GameSettings.getSettingsLocation(), "w")
        self._config.write(f)
        f.close()
