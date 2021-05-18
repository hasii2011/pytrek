from logging import Logger
from logging import getLogger

from pytrek.settings.BaseSubSetting import BaseSubSetting
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.SettingsCommon import SettingsNameValues


class DebugSettings(BaseSubSetting):

    DEBUG_SECTION: str = 'Debug'

    DEBUG_ADD_KLINGONS:  str = 'debug_add_klingons'
    DEBUG_KLINGON_COUNT: str = 'debug_klingon_count'

    DEBUG_SETTINGS: SettingsNameValues = {
        DEBUG_ADD_KLINGONS:     'False',
        DEBUG_KLINGON_COUNT:     '2'
    }

    def init(self, *args, **kwds):
        """
        This is a singleton based on the inheritance hierarchy
        """
        self.logger: Logger = getLogger(__name__)

        BaseSubSetting.init(self, *args, **kwds)

        self._settingsCommon: SettingsCommon = SettingsCommon(self._config)

    def addMissingSettings(self):
        self._settingsCommon.addMissingSettings(sectionName=DebugSettings.DEBUG_SECTION, nameValues=DebugSettings.DEBUG_SETTINGS)

    @property
    def debugKlingonCount(self) -> int:
        return self._config.getint(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_KLINGON_COUNT)

    @debugKlingonCount.setter
    def debugKlingonCount(self, newValue: int):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_KLINGON_COUNT, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def debugAddKlingons(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_ADD_KLINGONS)

    @debugAddKlingons.setter
    def debugAddKlingons(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_ADD_KLINGONS, str(newValue))
        self._settingsCommon.saveSettings()
