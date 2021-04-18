
from typing import Dict
from typing import NewType

from sys import platform as sysPlatform

from os import getenv as osGetEnv
from os import sep as osSep

from pytrek.Constants import GAME_SETTINGS_FILE_NAME
from pytrek.Constants import THE_GREAT_MAC_PLATFORM

from pytrek.exceptions.GameSettingsLocationNotSet import GameSettingsLocationNotSet

from pytrek.settings.BaseSubSetting import BaseSubSetting

SettingsNameValues = NewType('SettingsNameValues', Dict[str, str])


class SettingsCommon(BaseSubSetting):

    settingsFileLocationAndName: str = None

    def init(self, *args, **kwds):

        BaseSubSetting.init(self, *args, **kwds)

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

    def addMissingSetting(self, sectionName: str, preferenceName: str, value: str):
        self._config.set(sectionName, preferenceName, value)
        self.saveConfig()

    def saveConfig(self):
        """
        Save data to the preferences file
        """
        f = open(SettingsCommon.getSettingsLocation(), "w")
        self._config.write(f)
        f.close()
