from logging import Logger
from logging import getLogger

from pytrek.settings.BaseSubSetting import BaseSubSetting
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.SettingsCommon import SettingsNameValues


class PowerSettings(BaseSubSetting):

    POWER_SECTION: str = 'Power'

    INITIAL_ENERGY_LEVEL:   str = 'initial_energy_level'
    INITIAL_SHIELD_ENERGY:  str = 'initial_shield_energy'
    MINIMUM_IMPULSE_ENERGY: str = 'minimum_impulse_energy'
    INITIAL_TORPEDO_COUNT:  str = 'initial_torpedo_count'
    DEFAULT_WARP_FACTOR:    str = 'default_warp_factor'

    POWER_SETTINGS:  SettingsNameValues = SettingsNameValues({
        INITIAL_ENERGY_LEVEL:   '5000',
        INITIAL_SHIELD_ENERGY:  '2500',
        INITIAL_TORPEDO_COUNT:  '10',
        MINIMUM_IMPULSE_ENERGY: '30',
        DEFAULT_WARP_FACTOR:    '3'
    })

    def init(self, *args, **kwds):
        """
        This is a singleton based on the inheritance hierarchy
        """
        self.logger: Logger = getLogger(__name__)

        BaseSubSetting.init(self, *args, **kwds)

        self._settingsCommon: SettingsCommon = SettingsCommon(self._config)

    def addMissingSettings(self):
        self._settingsCommon.addMissingSettings(sectionName=PowerSettings.POWER_SECTION, nameValues=PowerSettings.POWER_SETTINGS)

    @property
    def initialEnergyLevel(self) -> int:
        return self._config.getint(PowerSettings.POWER_SECTION, PowerSettings.INITIAL_ENERGY_LEVEL)

    @property
    def initialShieldEnergy(self) -> int:
        return self._config.getint(PowerSettings.POWER_SECTION, PowerSettings.INITIAL_SHIELD_ENERGY)

    @property
    def initialTorpedoCount(self) -> int:
        return self._config.getint(PowerSettings.POWER_SECTION, PowerSettings.INITIAL_TORPEDO_COUNT)

    @property
    def minimumImpulseEnergy(self) -> int:
        return self._config.getint(PowerSettings.POWER_SECTION, PowerSettings.MINIMUM_IMPULSE_ENERGY)
