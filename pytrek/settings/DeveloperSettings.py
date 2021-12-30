from logging import Logger
from logging import getLogger

from pytrek.settings.BaseSubSetting import BaseSubSetting
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.SettingsCommon import SettingsNameValues


class DeveloperSettings(BaseSubSetting):

    DEVELOPER_SECTION: str = 'Developer'

    MAX_STARBASE_SEARCHES:  str = 'max_starbase_searches'
    MAX_COMMANDER_SEARCHES: str = 'max_commander_searches'

    DEVELOPER_SETTINGS: SettingsNameValues = SettingsNameValues({
        MAX_STARBASE_SEARCHES:  '128',
        MAX_COMMANDER_SEARCHES: '128'
    })

    def init(self, *args, **kwds):
        """
        This is a singleton based on the inheritance hierarchy
        """
        self.logger: Logger = getLogger(__name__)

        BaseSubSetting.init(self, *args, **kwds)

        self._settingsCommon: SettingsCommon = SettingsCommon(self._config)

    def addMissingSettings(self):
        self._settingsCommon.addMissingSettings(sectionName=DeveloperSettings.DEVELOPER_SECTION, nameValues=DeveloperSettings.DEVELOPER_SETTINGS)

    @property
    def maxStarbaseSearches(self) -> int:
        return self._config.getint(DeveloperSettings.DEVELOPER_SECTION, DeveloperSettings.MAX_STARBASE_SEARCHES)

    @maxStarbaseSearches.setter
    def maxStarbaseSearches(self, newValue: int):
        self._config.set(DeveloperSettings.DEVELOPER_SECTION, DeveloperSettings.MAX_STARBASE_SEARCHES, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def maxCommanderSearches(self) -> int:
        return self._config.getint(DeveloperSettings.DEVELOPER_SECTION, DeveloperSettings.MAX_COMMANDER_SEARCHES)

    @maxCommanderSearches.setter
    def maxCommanderSearches(self, newValue: int):
        self._config.set(DeveloperSettings.DEVELOPER_SECTION, DeveloperSettings.MAX_COMMANDER_SEARCHES, str(newValue))
        self._settingsCommon.saveSettings()
