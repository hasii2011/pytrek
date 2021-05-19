
from logging import Logger
from logging import getLogger

from pytrek.settings.BaseSubSetting import BaseSubSetting
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.SettingsCommon import SettingsNameValues


class LimitsSettings(BaseSubSetting):

    LIMITS_SECTION: str = 'Limits'

    MAXIMUM_STARS:       str = 'maximum_stars'
    MINIMUM_STAR_BASES:  str = 'minimum_star_bases'
    MAXIMUM_STAR_BASES:  str = 'maximum_star_bases'
    MAXIMUM_PLANETS:     str = 'maximum_planets'

    LIMITS_SETTINGS:  SettingsNameValues = {
        MAXIMUM_STARS:      '4',
        MINIMUM_STAR_BASES: '2',
        MAXIMUM_STAR_BASES: '5',
        MAXIMUM_PLANETS:    '10'
    }

    """
    This is a singleton based on the inheritance hierarchy
    """
    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        BaseSubSetting.init(self, *args, **kwds)

        self._settingsCommon: SettingsCommon = SettingsCommon(self._config)

    def addMissingSettings(self):
        self._settingsCommon.addMissingSettings(sectionName=LimitsSettings.LIMITS_SECTION, nameValues=LimitsSettings.LIMITS_SETTINGS)

    @property
    def maximumStars(self) -> int:
        return self._config.getint(LimitsSettings.LIMITS_SECTION, LimitsSettings.MAXIMUM_STARS)

    @property
    def minimumStarBases(self) -> int:
        return self._config.getint(LimitsSettings.LIMITS_SECTION, LimitsSettings.MINIMUM_STAR_BASES)

    @property
    def maximumStarBases(self) -> int:
        return self._config.getint(LimitsSettings.LIMITS_SECTION, LimitsSettings.MAXIMUM_STAR_BASES)

    @property
    def maximumPlanets(self) -> int:
        return self._config.getint(LimitsSettings.LIMITS_SECTION, LimitsSettings.MAXIMUM_PLANETS)
