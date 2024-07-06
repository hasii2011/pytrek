from logging import Logger
from logging import getLogger

from pytrek.model.Coordinates import Coordinates
from pytrek.settings.BaseSubSetting import BaseSubSetting
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.SettingsCommon import SettingsNameValues


class DebugSettings(BaseSubSetting):

    DEBUG_SECTION: str = 'Debug'

    MANUAL_PLACE_SHIP_IN_QUADRANT: str = 'manual_place_ship_in_quadrant'
    MANUAL_SECTOR_COORDINATES:     str = 'manual_sector_coordinates'
    ADD_KLINGONS:             str = 'add_klingons'
    KLINGON_COUNT:            str = 'klingon_count'
    ADD_COMMANDERS:           str = 'add_commanders'
    COMMANDER_COUNT:          str = 'commander_count'
    ADD_SUPER_COMMANDERS:     str = 'add_super_commanders'
    SUPER_COMMANDER_COUNT:    str = 'super_commander_count'
    PRINT_KLINGON_PLACEMENT:  str = 'print_klingon_placement'
    ADD_PLANET:               str = 'add_planet'
    ADD_STAR_BASE:            str = 'add_star_base'
    NO_KLINGONS:              str = 'no_klingons'
    NO_COMMANDERS:            str = 'no_commanders'
    NO_SUPER_COMMANDERS:      str = 'no_super_commanders'

    COLLECT_KLINGON_QUADRANT_COORDINATES:         str = 'collect_klingon_quadrant_coordinates'
    COLLECT_COMMANDER_QUADRANT_COORDINATES:       str = 'collect_commander_quadrant_coordinates'
    COLLECT_SUPER_COMMANDER_QUADRANT_COORDINATES: str = 'collect_super_commander_quadrant_coordinates'
    ANNOUNCE_QUADRANT_CREATION:                   str = 'announce_quadrant_creation'

    CONSOLE_SHOW_INTERNALS:          str = 'console_show_internals'
    SCHEDULE_SUPER_NOVA:             str = 'schedule_super_nova'
    SCHEDULE_TRACTOR_BEAM:           str = 'schedule_tractor_beam'
    SCHEDULE_COMMANDER_ATTACKS_BASE: str = 'schedule_commander_attacks_base'

    BASE_ENEMY_TORPEDO_DEBUG:          str = 'base_enemy_torpedo_debug'
    BASE_ENEMY_TORPEDO_DEBUG_INTERVAL: str = 'base_enemy_torpedo_debug_interval'
    SMOOTH_MOTION_DEBUG:               str = 'smooth_motion_debug'
    SMOOTH_MOTION_DEBUG_INTERVAL:      str = 'smooth_motion_debug_interval'

    DEBUG_SETTINGS: SettingsNameValues = SettingsNameValues({
        MANUAL_PLACE_SHIP_IN_QUADRANT: 'False',
        MANUAL_SECTOR_COORDINATES:     '0,0',
        ADD_KLINGONS:  'False',
        KLINGON_COUNT: '2',
        ADD_COMMANDERS: 'False',
        COMMANDER_COUNT: '2',
        ADD_SUPER_COMMANDERS: 'False',
        SUPER_COMMANDER_COUNT: '1',
        PRINT_KLINGON_PLACEMENT: 'False',
        COLLECT_KLINGON_QUADRANT_COORDINATES:         'False',
        COLLECT_COMMANDER_QUADRANT_COORDINATES:       'False',
        COLLECT_SUPER_COMMANDER_QUADRANT_COORDINATES: 'False',
        ANNOUNCE_QUADRANT_CREATION: 'False',
        ADD_PLANET:             'False',
        ADD_STAR_BASE:          'False',
        NO_KLINGONS:            'False',
        NO_COMMANDERS:          'False',
        NO_SUPER_COMMANDERS:    'False',
        CONSOLE_SHOW_INTERNALS: 'False',
        SCHEDULE_SUPER_NOVA:             'True',
        SCHEDULE_TRACTOR_BEAM:           'True',
        SCHEDULE_COMMANDER_ATTACKS_BASE: 'True',
        BASE_ENEMY_TORPEDO_DEBUG:          'False',
        BASE_ENEMY_TORPEDO_DEBUG_INTERVAL: '5',
        SMOOTH_MOTION_DEBUG:               'False',
        SMOOTH_MOTION_DEBUG_INTERVAL:      '5',
    })

    def __init__(self, **kwargs):
        """
        This is a singleton based on the inheritance hierarchy
        """
        self.logger: Logger = getLogger(__name__)

        super().__init__(**kwargs)

        self._settingsCommon: SettingsCommon = SettingsCommon()

    def addMissingSettings(self):
        self._settingsCommon.addMissingSettings(sectionName=DebugSettings.DEBUG_SECTION, nameValues=DebugSettings.DEBUG_SETTINGS)

    @property
    def manualPlaceShipInQuadrant(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.MANUAL_PLACE_SHIP_IN_QUADRANT)

    @manualPlaceShipInQuadrant.setter
    def manualPlaceShipInQuadrant(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.MANUAL_PLACE_SHIP_IN_QUADRANT, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def manualSectorCoordinates(self) -> Coordinates:
        values: str = self._config.get(DebugSettings.DEBUG_SECTION, DebugSettings.MANUAL_SECTOR_COORDINATES)
        return Coordinates.toCoordinates(values)

    @manualSectorCoordinates.setter
    def manualSectorCoordinates(self, newValue: Coordinates):
        values: str = f'{newValue.x},{newValue.y}'
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.MANUAL_SECTOR_COORDINATES, values)
        self._settingsCommon.saveSettings()

    @property
    def addKlingons(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.ADD_KLINGONS)

    @addKlingons.setter
    def addKlingons(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.ADD_KLINGONS, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def klingonCount(self) -> int:
        return self._config.getint(DebugSettings.DEBUG_SECTION, DebugSettings.KLINGON_COUNT)

    @klingonCount.setter
    def klingonCount(self, newValue: int):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.KLINGON_COUNT, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def addCommanders(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.ADD_COMMANDERS)

    @property
    def commanderCount(self) -> int:
        return self._config.getint(DebugSettings.DEBUG_SECTION, DebugSettings.COMMANDER_COUNT)

    @property
    def addSuperCommanders(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.ADD_SUPER_COMMANDERS)

    @property
    def superCommanderCount(self) -> int:
        return self._config.getint(DebugSettings.DEBUG_SECTION, DebugSettings.SUPER_COMMANDER_COUNT)

    @property
    def printKlingonPlacement(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.PRINT_KLINGON_PLACEMENT)

    @printKlingonPlacement.setter
    def printKlingonPlacement(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.PRINT_KLINGON_PLACEMENT, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def collectKlingonQuadrantCoordinates(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.COLLECT_KLINGON_QUADRANT_COORDINATES)

    @collectKlingonQuadrantCoordinates.setter
    def collectKlingonQuadrantCoordinates(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.COLLECT_KLINGON_QUADRANT_COORDINATES, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def collectCommanderQuadrantCoordinates(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.COLLECT_COMMANDER_QUADRANT_COORDINATES)

    @property
    def collectSuperCommanderQuadrantCoordinates(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.COLLECT_SUPER_COMMANDER_QUADRANT_COORDINATES)

    @property
    def announceQuadrantCreation(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.ANNOUNCE_QUADRANT_CREATION)

    @announceQuadrantCreation.setter
    def announceQuadrantCreation(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.ANNOUNCE_QUADRANT_CREATION, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def addPlanet(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.ADD_PLANET)

    @addPlanet.setter
    def addPlanet(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.ADD_PLANET, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def addStarBase(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.ADD_STAR_BASE)

    @addStarBase.setter
    def addStarBase(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.ADD_STAR_BASE, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def noKlingons(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.NO_KLINGONS)

    @noKlingons.setter
    def noKlingons(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.NO_KLINGONS, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def noCommanders(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.NO_COMMANDERS)

    @noCommanders.setter
    def noCommanders(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.NO_COMMANDERS, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def noSuperCommanders(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.NO_SUPER_COMMANDERS)

    @noSuperCommanders.setter
    def noSuperCommanders(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.NO_SUPER_COMMANDERS, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def consoleShowInternals(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.CONSOLE_SHOW_INTERNALS)

    @consoleShowInternals.setter
    def consoleShowInternals(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.CONSOLE_SHOW_INTERNALS, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def scheduleSuperNova(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.SCHEDULE_SUPER_NOVA)

    @scheduleSuperNova.setter
    def scheduleSuperNova(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.SCHEDULE_SUPER_NOVA, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def scheduleTractorBeam(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.SCHEDULE_TRACTOR_BEAM)

    @scheduleTractorBeam.setter
    def scheduleTractorBeam(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.SCHEDULE_TRACTOR_BEAM, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def scheduleCommanderAttacksBase(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.SCHEDULE_COMMANDER_ATTACKS_BASE)

    @scheduleCommanderAttacksBase.setter
    def scheduleCommanderAttacksBase(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.SCHEDULE_COMMANDER_ATTACKS_BASE, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def baseEnemyTorpedoDebug(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.BASE_ENEMY_TORPEDO_DEBUG)

    @baseEnemyTorpedoDebug.setter
    def baseEnemyTorpedoDebug(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.BASE_ENEMY_TORPEDO_DEBUG, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def baseEnemyTorpedoDebugInterval(self) -> int:
        return self._config.getint(DebugSettings.DEBUG_SECTION, DebugSettings.BASE_ENEMY_TORPEDO_DEBUG_INTERVAL)

    @baseEnemyTorpedoDebugInterval.setter
    def baseEnemyTorpedoDebugInterval(self, newValue: int):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.BASE_ENEMY_TORPEDO_DEBUG_INTERVAL, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def smoothMotionDebug(self) -> bool:
        return self._config.getboolean(DebugSettings.DEBUG_SECTION, DebugSettings.SMOOTH_MOTION_DEBUG)

    @smoothMotionDebug.setter
    def smoothMotionDebug(self, newValue: bool):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.SMOOTH_MOTION_DEBUG, str(newValue))
        self._settingsCommon.saveSettings()

    @property
    def smoothMotionDebugInterval(self) -> int:
        return self._config.getint(DebugSettings.DEBUG_SECTION, DebugSettings.SMOOTH_MOTION_DEBUG_INTERVAL)

    @smoothMotionDebugInterval.setter
    def smoothMotionDebugInterval(self, newValue: int):
        self._config.set(DebugSettings.DEBUG_SECTION, DebugSettings.SMOOTH_MOTION_DEBUG_INTERVAL, str(newValue))
        self._settingsCommon.saveSettings()
