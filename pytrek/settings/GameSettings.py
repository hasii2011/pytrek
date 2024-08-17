
from logging import Logger
from logging import getLogger

from codeallybasic.SecureConversions import SecureConversions

from codeallybasic.ConfigurationProperties import ConfigurationNameValue
from codeallybasic.ConfigurationProperties import ConfigurationProperties
from codeallybasic.ConfigurationProperties import PropertyName
from codeallybasic.ConfigurationProperties import Section
from codeallybasic.ConfigurationProperties import SectionName
from codeallybasic.ConfigurationProperties import Sections
from codeallybasic.ConfigurationProperties import configurationGetter
from codeallybasic.ConfigurationProperties import configurationSetter
from codeallybasic.SingletonV3 import SingletonV3

from pytrek.Constants import APPLICATION_NAME
from pytrek.engine.GameType import GameType
from pytrek.engine.PlayerType import PlayerType
from pytrek.model.Coordinates import Coordinates
from pytrek.settings.SoundVolume import SoundVolume
from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds

LIMITS_SECTION_NAME:     SectionName = SectionName('Limits')
POWER_SECTION_NAME:      SectionName = SectionName('Power')
GAME_LEVEL_SECTION_NAME: SectionName = SectionName('GameLevel')
FACTORS_SECTION_NAME:    SectionName = SectionName('Factors')
DEVELOPER_SECTION_NAME:  SectionName = SectionName('Developer')
DEBUG_SECTION_NAME:      SectionName = SectionName('Debug')
SPEED_SECTION_NAME:      SectionName = SectionName('TorpedoSpeeds')

SECTION_LIMITS: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('maximumStars'),       defaultValue='4'),
        ConfigurationNameValue(name=PropertyName('minimumStarBases'),   defaultValue='2'),
        ConfigurationNameValue(name=PropertyName('maximumStarBases'),   defaultValue='5'),
        ConfigurationNameValue(name=PropertyName('maximumPlanets'),     defaultValue='10'),
        ConfigurationNameValue(name=PropertyName('defaultFullShields'), defaultValue='2500'),
    ]
)


SECTION_POWER: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('initialEnergyLevel'),   defaultValue='5000'),
        ConfigurationNameValue(name=PropertyName('initialShieldEnergy'),  defaultValue='2500'),
        ConfigurationNameValue(name=PropertyName('initialTorpedoCount'),  defaultValue='10'),
        ConfigurationNameValue(name=PropertyName('minimumImpulseEnergy'), defaultValue='30'),
        ConfigurationNameValue(name=PropertyName('defaultWarpFactor'),    defaultValue='5'),
        ConfigurationNameValue(name=PropertyName('phaserFactor'),         defaultValue='2.0'),
    ]
)

SECTION_GAME_LEVEL: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('playerType'),  defaultValue=PlayerType.Good.name),
        ConfigurationNameValue(name=PropertyName('gameType'),    defaultValue=GameType.Short.name),
        ConfigurationNameValue(name=PropertyName('soundVolume'), defaultValue=SoundVolume.Medium.name),

    ]
)

SECTION_FACTORS: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('gameLengthFactor'),                defaultValue='64.0'),
        ConfigurationNameValue(name=PropertyName('starBaseExtender'),                defaultValue='2.0'),
        ConfigurationNameValue(name=PropertyName('starBaseMultiplier'),              defaultValue='3.0'),
        ConfigurationNameValue(name=PropertyName('minKlingonFiringInterval'),        defaultValue='7'),
        ConfigurationNameValue(name=PropertyName('maxKlingonFiringInterval'),        defaultValue='15'),
        ConfigurationNameValue(name=PropertyName('minCommanderFiringInterval'),      defaultValue='5'),
        ConfigurationNameValue(name=PropertyName('maxCommanderFiringInterval'),      defaultValue='10'),
        ConfigurationNameValue(name=PropertyName('minSuperCommanderFiringInterval'), defaultValue='5'),
        ConfigurationNameValue(name=PropertyName('maxSuperCommanderFiringInterval'), defaultValue='8'),
        ConfigurationNameValue(name=PropertyName('minKlingonMoveInterval'),          defaultValue='5'),
        ConfigurationNameValue(name=PropertyName('maxKlingonMoveInterval'),          defaultValue='12'),
        ConfigurationNameValue(name=PropertyName('minCommanderMoveInterval'),        defaultValue='3'),
        ConfigurationNameValue(name=PropertyName('maxCommanderMoveInterval'),        defaultValue='10'),
        ConfigurationNameValue(name=PropertyName('minSuperCommanderMoveInterval'),   defaultValue='3'),
        ConfigurationNameValue(name=PropertyName('maxSuperCommanderMoveInterval'),   defaultValue='7'),
        ConfigurationNameValue(name=PropertyName('basicMissDisplayInterval'),        defaultValue='5'),
        ConfigurationNameValue(name=PropertyName('photonTorpedoMisfireRate'),        defaultValue='0.2'),
        ConfigurationNameValue(name=PropertyName('phaserBurstToTerminate'),          defaultValue='20.0'),
    ]
)

SECTION_DEVELOPER: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('maxStarbaseSearches'),  defaultValue='128'),
        ConfigurationNameValue(name=PropertyName('maxCommanderSearches'), defaultValue='128'),
    ]
)


SECTION_DEBUG: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('manualPlaceShipInQuadrant'),                defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('manualSectorCoordinates'),                  defaultValue='0,0'),
        ConfigurationNameValue(name=PropertyName('addKlingons'),                              defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('klingonCount'),                             defaultValue='1'),
        ConfigurationNameValue(name=PropertyName('addCommanders'),                            defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('commanderCount'),                           defaultValue='1'),
        ConfigurationNameValue(name=PropertyName('addSuperCommanders'),                       defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('superCommanderCount'),                      defaultValue='1'),
        ConfigurationNameValue(name=PropertyName('printKlingonPlacement'),                    defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('addPlanet'),                                defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('addStarBase'),                              defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('noKlingons'),                               defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('noCommanders'),                             defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('noSuperCommanders'),                        defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('consoleShowInternals'),                     defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('scheduleSuperNova'),                        defaultValue='True'),
        ConfigurationNameValue(name=PropertyName('scheduleTractorBeam'),                      defaultValue='True'),
        ConfigurationNameValue(name=PropertyName('scheduleCommanderAttacksBase'),             defaultValue='True'),
        ConfigurationNameValue(name=PropertyName('collectKlingonQuadrantCoordinates'),        defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('collectCommanderQuadrantCoordinates'),      defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('collectSuperCommanderQuadrantCoordinates'), defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('announceQuadrantCreation'),                 defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('debugBaseEnemyTorpedo'),                    defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('debugBaseEnemyTorpedoInterval'),            defaultValue='20'),
        ConfigurationNameValue(name=PropertyName('debugSmoothMotion'),                        defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('debugSmoothMotionInterval'),                defaultValue='5'),
        ConfigurationNameValue(name=PropertyName('drawSectionBoundaries'),                    defaultValue='False'),
    ]
)

NOVICE_PLAYER:   str = PlayerType.Novice.name.lower()
FAIR_PLAYER:     str = PlayerType.Fair.name.lower()
GOOD_PLAYER:     str = PlayerType.Good.name.lower()
EXPERT_PLAYER:   str = PlayerType.Expert.name.lower()
EMERITUS_PLAYER: str = PlayerType.Emeritus.name.lower()

PROPERTY_NAME_SUFFIX: str = 'TorpedoSpeeds'

SECTION_SPEED_SETTINGS: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName(f'{NOVICE_PLAYER}{PROPERTY_NAME_SUFFIX}'),   defaultValue='5,2,2,1'),
        ConfigurationNameValue(name=PropertyName(f'{FAIR_PLAYER}{PROPERTY_NAME_SUFFIX}'),     defaultValue='4,2,2,1'),
        ConfigurationNameValue(name=PropertyName(f'{GOOD_PLAYER}{PROPERTY_NAME_SUFFIX}'),     defaultValue='3,2,3,4'),
        ConfigurationNameValue(name=PropertyName(f'{EXPERT_PLAYER}{PROPERTY_NAME_SUFFIX}'),   defaultValue='2,2,4,4'),
        ConfigurationNameValue(name=PropertyName(f'{EMERITUS_PLAYER}{PROPERTY_NAME_SUFFIX}'), defaultValue='1,2,5,5'),
    ]
)

GAME_SETTINGS_SECTIONS: Sections = Sections(
    {
        LIMITS_SECTION_NAME:     SECTION_LIMITS,
        POWER_SECTION_NAME:      SECTION_POWER,
        GAME_LEVEL_SECTION_NAME: SECTION_GAME_LEVEL,
        FACTORS_SECTION_NAME:    SECTION_FACTORS,
        SPEED_SECTION_NAME:      SECTION_SPEED_SETTINGS,
        DEVELOPER_SECTION_NAME:  SECTION_DEVELOPER,
        DEBUG_SECTION_NAME:      SECTION_DEBUG,
    }
)


class GameSettings(ConfigurationProperties, metaclass=SingletonV3):
    """
    The `getters` in this class appear to return some value.  This is just to
    stop PyCharm and mypy from complaining.  In reality, the `getters` are never called
    and the value is returned from the configuration file
    """

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        super().__init__(baseFileName='pytrek.ini', moduleName=APPLICATION_NAME, sections=GAME_SETTINGS_SECTIONS)

        self._configParser.optionxform = self._toStr    # type: ignore
        self._loadConfiguration()

    @property
    @configurationGetter(sectionName=LIMITS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def maximumStars(self) -> int:
        return 0        # Never used

    @property
    @configurationGetter(sectionName=LIMITS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def minimumStarBases(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=LIMITS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def maximumStarBases(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=LIMITS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def maximumPlanets(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=LIMITS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def defaultFullShields(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=POWER_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def initialEnergyLevel(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=POWER_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def initialShieldEnergy(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=POWER_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def initialTorpedoCount(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=POWER_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def minimumImpulseEnergy(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=POWER_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def defaultWarpFactor(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=POWER_SECTION_NAME, deserializeFunction=SecureConversions.secureFloat)
    def phaserFactor(self) -> float:
        return 0.0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureFloat)
    def gameLengthFactor(self) -> float:
        return 0.0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureFloat)
    def starBaseExtender(self) -> float:
        return 0.0

    @property
    @configurationGetter(sectionName=GAME_LEVEL_SECTION_NAME, deserializeFunction=PlayerType.toEnum)
    def playerType(self) -> PlayerType:
        return PlayerType.Novice        # value not used

    @playerType.setter
    @configurationSetter(sectionName=GAME_LEVEL_SECTION_NAME, enumUseName=True)
    def playerType(self, newValue: PlayerType):
        pass

    @property
    @configurationGetter(sectionName=GAME_LEVEL_SECTION_NAME, deserializeFunction=GameType.toEnum)
    def gameType(self) -> GameType:
        return GameType.Short       # Value never used

    @gameType.setter
    @configurationSetter(sectionName=GAME_LEVEL_SECTION_NAME, enumUseName=True)
    def gameType(self, newValue: GameType):
        pass

    @property
    @configurationGetter(sectionName=GAME_LEVEL_SECTION_NAME, deserializeFunction=SoundVolume.toEnum)
    def soundVolume(self) -> SoundVolume:
        return SoundVolume.Medium       # value never used

    @soundVolume.setter
    @configurationSetter(sectionName=GAME_LEVEL_SECTION_NAME, enumUseName=True)
    def soundVolume(self, newValue: SoundVolume):
        pass

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureFloat)
    def starBaseMultiplier(self) -> float:
        return 0.0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def minKlingonFiringInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def maxKlingonFiringInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def minCommanderFiringInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def maxCommanderFiringInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def minSuperCommanderFiringInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def maxSuperCommanderFiringInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def minKlingonMoveInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def maxKlingonMoveInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def minCommanderMoveInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def maxCommanderMoveInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def minSuperCommanderMoveInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def maxSuperCommanderMoveInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def basicMissDisplayInterval(self) -> int:
        return 0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureFloat)
    def photonTorpedoMisfireRate(self) -> float:
        return 0.0

    @property
    @configurationGetter(sectionName=FACTORS_SECTION_NAME, deserializeFunction=SecureConversions.secureFloat)
    def phaserBurstToTerminate(self) -> float:
        return 0.0

    @property
    @configurationGetter(sectionName=SPEED_SECTION_NAME, deserializeFunction=TorpedoSpeeds.toTorpedoSpeed)
    def noviceTorpedoSpeeds(self) -> TorpedoSpeeds:
        return TorpedoSpeeds()

    @property
    @configurationGetter(sectionName=SPEED_SECTION_NAME, deserializeFunction=TorpedoSpeeds.toTorpedoSpeed)
    def fairTorpedoSpeeds(self) -> TorpedoSpeeds:
        return TorpedoSpeeds()

    @property
    @configurationGetter(sectionName=SPEED_SECTION_NAME, deserializeFunction=TorpedoSpeeds.toTorpedoSpeed)
    def goodTorpedoSpeeds(self) -> TorpedoSpeeds:
        return TorpedoSpeeds()

    @property
    @configurationGetter(sectionName=SPEED_SECTION_NAME, deserializeFunction=TorpedoSpeeds.toTorpedoSpeed)
    def expertTorpedoSpeeds(self) -> TorpedoSpeeds:
        return TorpedoSpeeds()

    @property
    @configurationGetter(sectionName=SPEED_SECTION_NAME, deserializeFunction=TorpedoSpeeds.toTorpedoSpeed)
    def emeritusTorpedoSpeeds(self) -> TorpedoSpeeds:
        return TorpedoSpeeds()

    @property
    @configurationGetter(sectionName=DEVELOPER_SECTION_NAME, deserializeFunction=SecureConversions.secureFloat)
    def maxStarbaseSearches(self) -> int:
        return 0

    @maxStarbaseSearches.setter
    @configurationSetter(sectionName=DEVELOPER_SECTION_NAME)
    def maxStarbaseSearches(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=DEVELOPER_SECTION_NAME, deserializeFunction=SecureConversions.secureFloat)
    def maxCommanderSearches(self) -> int:
        return 0

    @maxCommanderSearches.setter
    @configurationSetter(sectionName=DEVELOPER_SECTION_NAME)
    def maxCommanderSearches(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def manualPlaceShipInQuadrant(self) -> bool:
        return False

    @manualPlaceShipInQuadrant.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def manualPlaceShipInQuadrant(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=Coordinates.toCoordinates)
    def manualSectorCoordinates(self) -> Coordinates:
        return Coordinates(0, 0)

    @manualSectorCoordinates.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def manualSectorCoordinates(self, newValue: Coordinates):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def addKlingons(self) -> bool:
        return False

    @addKlingons.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def addKlingons(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def klingonCount(self) -> int:
        return 0

    @klingonCount.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def klingonCount(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def addCommanders(self) -> bool:
        return True

    @addCommanders.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def addCommanders(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def commanderCount(self) -> int:
        return 0

    @commanderCount.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def commanderCount(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def addSuperCommanders(self) -> bool:
        return False

    @addSuperCommanders.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def addSuperCommanders(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def superCommanderCount(self) -> int:
        return 0

    @superCommanderCount.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def superCommanderCount(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def printKlingonPlacement(self) -> bool:
        return False

    @printKlingonPlacement.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def printKlingonPlacement(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def addPlanet(self) -> bool:
        return False

    @addPlanet.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def addPlanet(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def addStarBase(self) -> bool:
        return False

    @addStarBase.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def addStarBase(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def noKlingons(self) -> bool:
        return False

    @noKlingons.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def noKlingons(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def noCommanders(self) -> bool:
        return False

    @noCommanders.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def noCommanders(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def noSuperCommanders(self) -> bool:
        return False

    @noSuperCommanders.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def noSuperCommanders(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def consoleShowInternals(self) -> bool:
        return False

    @consoleShowInternals.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def consoleShowInternals(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def scheduleSuperNova(self) -> bool:
        return False

    @scheduleSuperNova.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def scheduleSuperNova(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def scheduleTractorBeam(self) -> bool:
        return False

    @scheduleTractorBeam.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def scheduleTractorBeam(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def scheduleCommanderAttacksBase(self) -> bool:
        return False

    @scheduleCommanderAttacksBase.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def scheduleCommanderAttacksBase(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def collectKlingonQuadrantCoordinates(self) -> bool:
        return False

    @collectKlingonQuadrantCoordinates.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def collectKlingonQuadrantCoordinates(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def collectCommanderQuadrantCoordinates(self) -> bool:
        return False

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def collectSuperCommanderQuadrantCoordinates(self) -> bool:
        return False

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def announceQuadrantCreation(self) -> bool:
        return False

    @announceQuadrantCreation.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def announceQuadrantCreation(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def debugBaseEnemyTorpedo(self) -> bool:
        return False

    @debugBaseEnemyTorpedo.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def debugBaseEnemyTorpedo(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def debugBaseEnemyTorpedoInterval(self) -> int:
        return 0

    @debugBaseEnemyTorpedoInterval.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def debugBaseEnemyTorpedoInterval(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def debugSmoothMotion(self) -> bool:
        return False

    @debugSmoothMotion.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def debugSmoothMotion(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureInteger)
    def debugSmoothMotionInterval(self) -> int:
        return 0

    @debugSmoothMotionInterval.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def debugSmoothMotionInterval(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def drawSectionBoundaries(self) -> bool:
        return False        # never used

    @drawSectionBoundaries.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def drawSectionBoundaries(self, value: bool):
        pass

    def _toStr(self, optionString: str) -> str:
        """
        Override base method

        Args:
            optionString:

        Returns: The option string unchanged
        """
        return optionString
