
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

    MIN_KLINGON_FIRING_INTERVAL:   str = 'min_klingon_firing_interval'
    MAX_KLINGON_FIRING_INTERVAL:   str = 'max_klingon_firing_interval'
    MIN_COMMANDER_FIRING_INTERVAL: str = 'min_commander_firing_interval'
    MAX_COMMANDER_FIRING_INTERVAL: str = 'max_commander_firing_interval'
    MIN_SUPER_COMMANDER_FIRING_INTERVAL: str = 'min_super_commander_firing_interval'
    MAX_SUPER_COMMANDER_FIRING_INTERVAL: str = 'max_super_commander_firing_interval'

    MIN_KLINGON_MOVE_INTERVAL:   str = 'min_klingon_move_interval'
    MAX_KLINGON_MOVE_INTERVAL:   str = 'max_klingon_move_interval'
    MIN_COMMANDER_MOVE_INTERVAL: str = 'min_commander_move_interval'
    MAX_COMMANDER_MOVE_INTERVAL: str = 'max_commander_move_interval'
    MIN_SUPER_COMMANDER_MOVE_INTERVAL: str = 'min_super_commander_move_interval'
    MAX_SUPER_COMMANDER_MOVE_INTERVAL: str = 'max_super_commander_move_interval'

    BASIC_MISS_DISPLAY_INTERVAL: str = 'basic_miss_display_interval'
    PHOTON_TORPEDO_MISFIRE_RATE: str = 'photon_torpedo_misfire_rate'
    PHASER_BURST_TO_TERMINATE:   str = 'phaser_burst_to_terminate'

    FACTORS_SETTINGS: SettingsNameValues = SettingsNameValues({
        GAME_LENGTH_FACTOR:     '7.0',
        STAR_BASE_EXTENDER:     '2.0',
        STAR_BASE_MULTIPLIER:   '3.0',

        MIN_KLINGON_FIRING_INTERVAL: '7',
        MAX_KLINGON_FIRING_INTERVAL: '15',

        MIN_COMMANDER_FIRING_INTERVAL: '5',
        MAX_COMMANDER_FIRING_INTERVAL: '10',

        MIN_SUPER_COMMANDER_FIRING_INTERVAL: '5',
        MAX_SUPER_COMMANDER_FIRING_INTERVAL: '8',

        MIN_KLINGON_MOVE_INTERVAL:    '5',
        MAX_KLINGON_MOVE_INTERVAL:    '12',

        MIN_COMMANDER_MOVE_INTERVAL: '3',
        MAX_COMMANDER_MOVE_INTERVAL: '10',

        MIN_SUPER_COMMANDER_MOVE_INTERVAL: '3',
        MAX_SUPER_COMMANDER_MOVE_INTERVAL: '7',

        BASIC_MISS_DISPLAY_INTERVAL: '5',
        PHOTON_TORPEDO_MISFIRE_RATE: '0.2',
        PHASER_BURST_TO_TERMINATE: '20.0'
    })

    # noinspection SpellCheckingInspection
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

    @property
    def minCommanderFiringInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MIN_COMMANDER_FIRING_INTERVAL)

    @property
    def maxCommanderFiringInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MAX_COMMANDER_FIRING_INTERVAL)

    @property
    def minSuperCommanderFiringInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MIN_SUPER_COMMANDER_FIRING_INTERVAL)

    @property
    def maxSuperCommanderFiringInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MAX_SUPER_COMMANDER_FIRING_INTERVAL)

    @property
    def minKlingonMoveInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MIN_KLINGON_MOVE_INTERVAL)

    @property
    def maxKlingonMoveInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MAX_KLINGON_MOVE_INTERVAL)

    @property
    def minCommanderMoveInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MIN_COMMANDER_MOVE_INTERVAL)

    @property
    def maxCommanderMoveInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MAX_COMMANDER_MOVE_INTERVAL)

    @property
    def minSuperCommanderMoveInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MIN_SUPER_COMMANDER_MOVE_INTERVAL)

    @property
    def maxSuperCommanderMoveInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.MAX_SUPER_COMMANDER_MOVE_INTERVAL)

    @property
    def basicMissDisplayInterval(self) -> int:
        return self._config.getint(FactorsSettings.FACTORS_SECTION, FactorsSettings.BASIC_MISS_DISPLAY_INTERVAL)

    @property
    def photonTorpedoMisfireRate(self) -> float:
        return self._config.getfloat(FactorsSettings.FACTORS_SECTION, FactorsSettings.PHOTON_TORPEDO_MISFIRE_RATE)

    @property
    def phaserBurstToTerminate(self) -> float:
        return self._config.getfloat(FactorsSettings.FACTORS_SECTION, FactorsSettings.PHASER_BURST_TO_TERMINATE)
