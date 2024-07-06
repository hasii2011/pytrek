
from typing import Dict
from typing import NewType

from logging import Logger
from logging import getLogger

from sys import platform as sysPlatform

from os import getenv as osGetEnv
from os import sep as osSep
from typing import cast

from pytrek.Constants import GAME_SETTINGS_FILE_NAME
from pytrek.Constants import THE_GREAT_MAC_PLATFORM

from pytrek.exceptions.GameSettingsLocationNotSet import GameSettingsLocationNotSet

from pytrek.settings.BaseSubSetting import BaseSubSetting

SettingsNameValues = NewType('SettingsNameValues', Dict[str, str])


class SettingsCommon(BaseSubSetting):

    settingsFileLocationAndName: str = cast(str, None)

    def __init__(self, **kwargs):

        self.logger: Logger = getLogger(__name__)
        super().__init__(**kwargs)

    @classmethod
    def determineSettingsLocation(cls):
        """
        This method MUST (I repeat MUST) be called before attempting to instantiate the game settings Singleton
        """
        if sysPlatform == "linux2" or sysPlatform == "linux" or sysPlatform == THE_GREAT_MAC_PLATFORM:
            SettingsCommon.settingsFileLocationAndName = f'{osGetEnv("HOME")}{osSep}{GAME_SETTINGS_FILE_NAME}'
        else:
            SettingsCommon.settingsFileLocationAndName = GAME_SETTINGS_FILE_NAME

    @classmethod
    def getSettingsLocation(cls):
        if SettingsCommon.settingsFileLocationAndName is None:
            raise GameSettingsLocationNotSet()
        else:
            return SettingsCommon.settingsFileLocationAndName

    def addMissingSettings(self, sectionName: str, nameValues: SettingsNameValues):
        try:
            if self._config.has_section(sectionName) is False:
                self.logger.warning(f'Missing section: {sectionName}')
                self._config.add_section(sectionName)

            for settingName in nameValues.keys():
                if self._config.has_option(sectionName, settingName) is False:
                    self.logger.warning(f'Missing setting: {settingName}')
                    self.addMissingSetting(sectionName, settingName, nameValues[settingName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    def addMissingSetting(self, sectionName: str, preferenceName: str, value: str):
        self._config.set(sectionName, preferenceName, value)
        self.saveSettings()

    def saveSettings(self):
        """
        Save data to the settings file
        """
        f = open(SettingsCommon.getSettingsLocation(), "w")
        self._config.write(f)
        f.close()
