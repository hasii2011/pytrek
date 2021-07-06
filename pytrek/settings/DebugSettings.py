from logging import Logger
from logging import getLogger

from pytrek.settings.BaseSubSetting import BaseSubSetting
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.SettingsCommon import SettingsNameValues


class DebugSettings(BaseSubSetting):

    DEBUG_SECTION: str = 'Debug'

    DEBUG_ADD_KLINGONS:             str = 'debug_add_klingons'
    DEBUG_KLINGON_COUNT:            str = 'debug_klingon_count'
    DEBUG_ADD_COMMANDERS:           str = 'debug_add_commanders'
    DEBUG_COMMANDER_COUNT:          str = 'debug_commander_count'
    DEBUG_ADD_SUPER_COMMANDERS:     str = 'debug_add_super_commanders'
    DEBUG_SUPER_COMMANDER_COUNT:    str = 'debug_super_commander_count'
    DEBUG_PRINT_KLINGON_PLACEMENT:  str = 'debug_print_klingon_placement'
    DEBUG_ADD_PLANET:               str = 'debug_add_planet'

    DEBUG_COLLECT_KLINGON_QUADRANT_COORDINATES:         str = 'debug_collect_klingon_quadrant_coordinates'
    DEBUG_COLLECT_COMMANDER_QUADRANT_COORDINATES:       str = 'debug_collect_commander_quadrant_coordinates'
    DEBUG_COLLECT_SUPER_COMMANDER_QUADRANT_COORDINATES: str = 'debug_collect_super_commander_quadrant_coordinates'
    DEBUG_ANNOUNCE_QUADRANT_CREATION:                   str = 'debug_announce_quadrant_creation'

    DEBUG_SETTINGS: SettingsNameValues = SettingsNameValues({
        DEBUG_ADD_KLINGONS:             'False',
        DEBUG_KLINGON_COUNT:            '2',
        DEBUG_ADD_COMMANDERS:           'False',
        DEBUG_COMMANDER_COUNT:          '2',
        DEBUG_ADD_SUPER_COMMANDERS:     'False',
        DEBUG_SUPER_COMMANDER_COUNT:    '1',
        DEBUG_PRINT_KLINGON_PLACEMENT:  'False',
        DEBUG_COLLECT_KLINGON_QUADRANT_COORDINATES:         'False',
        DEBUG_COLLECT_COMMANDER_QUADRANT_COORDINATES:       'False',
        DEBUG_COLLECT_SUPER_COMMANDER_QUADRANT_COORDINATES: 'False',
        DEBUG_ANNOUNCE_QUADRANT_CREATION:           'False',
        DEBUG_ADD_PLANET:                           'False',
    })

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
    def debugAddKlingons(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_ADD_KLINGONS)

    @debugAddKlingons.setter
    def debugAddKlingons(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_ADD_KLINGONS, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def debugKlingonCount(self) -> int:
        return self._config.getint(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_KLINGON_COUNT)

    @debugKlingonCount.setter
    def debugKlingonCount(self, newValue: int):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_KLINGON_COUNT, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def debugAddCommanders(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_ADD_COMMANDERS)

    @property
    def debugCommanderCount(self) -> int:
        return self._config.getint(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_COMMANDER_COUNT)

    @property
    def debugAddSuperCommanders(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_ADD_SUPER_COMMANDERS)

    @property
    def debugSuperCommanderCount(self) -> int:
        return self._config.getint(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_SUPER_COMMANDER_COUNT)

    @property
    def debugPrintKlingonPlacement(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_PRINT_KLINGON_PLACEMENT)

    @debugPrintKlingonPlacement.setter
    def debugPrintKlingonPlacement(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_PRINT_KLINGON_PLACEMENT, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def debugCollectKlingonQuadrantCoordinates(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_COLLECT_KLINGON_QUADRANT_COORDINATES)

    @debugCollectKlingonQuadrantCoordinates.setter
    def debugCollectKlingonQuadrantCoordinates(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_COLLECT_KLINGON_QUADRANT_COORDINATES, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def debugCollectCommanderQuadrantCoordinates(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_COLLECT_COMMANDER_QUADRANT_COORDINATES)

    @property
    def debugCollectSuperCommanderQuadrantCoordinates(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_COLLECT_SUPER_COMMANDER_QUADRANT_COORDINATES)

    @property
    def debugAnnounceQuadrantCreation(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_ANNOUNCE_QUADRANT_CREATION)

    @debugAnnounceQuadrantCreation.setter
    def debugAnnounceQuadrantCreation(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_ANNOUNCE_QUADRANT_CREATION, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def debugAddPlanet(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_ADD_PLANET)

    @debugAddPlanet.setter
    def debugAddPlanet(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.DEBUG_ADD_PLANET, str(newValue))
        self._settingsCommon.saveSettings()
