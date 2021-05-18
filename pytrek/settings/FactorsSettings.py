
from logging import Logger
from logging import getLogger

from pytrek.settings.BaseSubSetting import BaseSubSetting
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.SettingsCommon import SettingsNameValues


class FactorsSettings(BaseSubSetting):

    FACTORS_SECTION: str = 'Factors'

    GAME_LENGTH_FACTOR:   str = 'game_length_factor'
    STAR_BASE_EXTENDER:   str = 'star_base_extender'
    STAR_BASE_MULTIPLIER: str = 'star_base_multiplier'

    MIN_KLINGON_FIRING_INTERVAL: str = 'min_klingon_firing_interval'
    MAX_KLINGON_FIRING_INTERVAL: str = 'max_klingon_firing_interval'

    FACTORS_SETTINGS: SettingsNameValues = {
        GAME_LENGTH_FACTOR:     '7.0',
        STAR_BASE_EXTENDER:     '2.0',
        STAR_BASE_MULTIPLIER:   '3.0',
        MIN_KLINGON_FIRING_INTERVAL: '7',
        MAX_KLINGON_FIRING_INTERVAL: '15'
    }

    def init(self, *args, **kwds):
        """
        This is a singleton based on the inheritance hierarchy
        """
        self.logger: Logger = getLogger(__name__)

        BaseSubSetting.init(self, *args, **kwds)

        self._settingsCommon: SettingsCommon = SettingsCommon(self._config)

    def addMissingSettings(self):
        self._settingsCommon.addMissingSettings(sectionName=FactorsSettings.FACTORS_SECTION, nameValues=FactorsSettings.FACTORS_SETTINGS)

    @property
    def gameLengthFactor(self) -> float:
        return self._config.getfloat(FactorsSettings.FACTORS_SECTION, FactorsSettings.GAME_LENGTH_FACTOR)

    @property
    def starBaseExtender(self) -> float:
        return self._config.getfloat(FactorsSettings.FACTORS_SECTION, FactorsSettings.STAR_BASE_EXTENDER)

    @property
    def starBaseMultiplier(self) -> float:
        return self._config.getfloat(FactorsSettings.FACTORS_SECTION, FactorsSettings.STAR_BASE_MULTIPLIER)

    @property
    def minKlingonFiringInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MIN_KLINGON_FIRING_INTERVAL)

    @property
    def maxKlingonFiringInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MAX_KLINGON_FIRING_INTERVAL)
