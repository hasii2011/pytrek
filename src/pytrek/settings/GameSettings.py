
from logging import Logger
from logging import getLogger

from codeallybasic.DynamicConfiguration import KeyName
from codeallybasic.DynamicConfiguration import SectionName
from codeallybasic.DynamicConfiguration import Sections
from codeallybasic.DynamicConfiguration import ValueDescription
from codeallybasic.DynamicConfiguration import ValueDescriptions
from codeallybasic.SecureConversions import SecureConversions
from codeallybasic.DynamicConfiguration import DynamicConfiguration
from codeallybasic.SingletonV3 import SingletonV3

from pytrek.Constants import APPLICATION_NAME
from pytrek.Constants import GAME_SETTINGS_FILE_NAME

from pytrek.engine.GameType import GameType
from pytrek.engine.PlayerType import PlayerType
from pytrek.model.Coordinates import Coordinates
from pytrek.settings.SoundVolume import SoundVolume
from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds

SECTION_LIMITS: ValueDescriptions = ValueDescriptions(
    {
        KeyName('maximumStars'):       ValueDescription(defaultValue='4',    deserializer=SecureConversions.secureInteger),
        KeyName('minimumStarBases'):   ValueDescription(defaultValue='2',    deserializer=SecureConversions.secureInteger),
        KeyName('maximumStarBases'):   ValueDescription(defaultValue='5',    deserializer=SecureConversions.secureInteger),
        KeyName('maximumPlanets'):     ValueDescription(defaultValue='10',   deserializer=SecureConversions.secureInteger),
        KeyName('defaultFullShields'): ValueDescription(defaultValue='2500', deserializer=SecureConversions.secureInteger),
    }
)


SECTION_POWER: ValueDescriptions = ValueDescriptions(
    {
        KeyName('initialEnergyLevel'):   ValueDescription(defaultValue='5000', deserializer=SecureConversions.secureInteger),
        KeyName('initialShieldEnergy'):  ValueDescription(defaultValue='2500', deserializer=SecureConversions.secureInteger),
        KeyName('initialTorpedoCount'):  ValueDescription(defaultValue='10',   deserializer=SecureConversions.secureInteger),
        KeyName('minimumImpulseEnergy'): ValueDescription(defaultValue='30',   deserializer=SecureConversions.secureInteger),
        KeyName('defaultWarpFactor'):    ValueDescription(defaultValue='5',    deserializer=SecureConversions.secureInteger),
        KeyName('phaserFactor'):         ValueDescription(defaultValue='2.0',  deserializer=SecureConversions.secureFloat),
    }
)

SECTION_GAME_LEVEL: ValueDescriptions = ValueDescriptions(
    {
        KeyName('playerType'):  ValueDescription(defaultValue=PlayerType.Good.name,     enumUseName=True, deserializer=PlayerType.toEnum),
        KeyName('gameType'):    ValueDescription(defaultValue=GameType.Short.name,      enumUseName=True, deserializer=GameType.toEnum),
        KeyName('soundVolume'): ValueDescription(defaultValue=SoundVolume.Medium.name,  enumUseName=True, deserializer=SoundVolume.toEnum),
    }
)

SECTION_FACTORS: ValueDescriptions = ValueDescriptions(
    {
        KeyName('gameLengthFactor'):                ValueDescription(defaultValue='64.0', deserializer=SecureConversions.secureFloat),
        KeyName('starBaseExtender'):                ValueDescription(defaultValue='2.0',  deserializer=SecureConversions.secureFloat),
        KeyName('starBaseMultiplier'):              ValueDescription(defaultValue='3.0',  deserializer=SecureConversions.secureFloat),
        KeyName('minKlingonFiringInterval'):        ValueDescription(defaultValue='7',    deserializer=SecureConversions.secureInteger),
        KeyName('maxKlingonFiringInterval'):        ValueDescription(defaultValue='15',   deserializer=SecureConversions.secureInteger),
        KeyName('minCommanderFiringInterval'):      ValueDescription(defaultValue='5',    deserializer=SecureConversions.secureInteger),
        KeyName('maxCommanderFiringInterval'):      ValueDescription(defaultValue='10',   deserializer=SecureConversions.secureInteger),
        KeyName('minSuperCommanderFiringInterval'): ValueDescription(defaultValue='5',    deserializer=SecureConversions.secureInteger),
        KeyName('maxSuperCommanderFiringInterval'): ValueDescription(defaultValue='8',    deserializer=SecureConversions.secureInteger),
        KeyName('minKlingonMoveInterval'):          ValueDescription(defaultValue='5',    deserializer=SecureConversions.secureInteger),
        KeyName('maxKlingonMoveInterval'):          ValueDescription(defaultValue='12',   deserializer=SecureConversions.secureInteger),
        KeyName('minCommanderMoveInterval'):        ValueDescription(defaultValue='3',    deserializer=SecureConversions.secureInteger),
        KeyName('maxCommanderMoveInterval'):        ValueDescription(defaultValue='10',   deserializer=SecureConversions.secureInteger),
        KeyName('minSuperCommanderMoveInterval'):   ValueDescription(defaultValue='3',    deserializer=SecureConversions.secureInteger),
        KeyName('maxSuperCommanderMoveInterval'):   ValueDescription(defaultValue='7',    deserializer=SecureConversions.secureInteger),
        KeyName('basicMissDisplayInterval'):        ValueDescription(defaultValue='5',    deserializer=SecureConversions.secureInteger),
        KeyName('photonTorpedoMisfireRate'):        ValueDescription(defaultValue='0.2',  deserializer=SecureConversions.secureFloat),
        KeyName('phaserBurstToTerminate'):          ValueDescription(defaultValue='20.0', deserializer=SecureConversions.secureFloat),
        KeyName('damageAdjuster'):                  ValueDescription(defaultValue='0.5',  deserializer=SecureConversions.secureFloat),
    }
)

NOVICE_PLAYER:   str = PlayerType.Novice.name.lower()
FAIR_PLAYER:     str = PlayerType.Fair.name.lower()
GOOD_PLAYER:     str = PlayerType.Good.name.lower()
EXPERT_PLAYER:   str = PlayerType.Expert.name.lower()
EMERITUS_PLAYER: str = PlayerType.Emeritus.name.lower()

KEY_NAME_SUFFIX: str = 'TorpedoSpeeds'

SECTION_SPEED_SETTINGS: ValueDescriptions = ValueDescriptions(
    {
        KeyName(f'{NOVICE_PLAYER}{KEY_NAME_SUFFIX}'):   ValueDescription(defaultValue='5,2,2,1', deserializer=TorpedoSpeeds.toTorpedoSpeed),
        KeyName(f'{FAIR_PLAYER}{KEY_NAME_SUFFIX}'):     ValueDescription(defaultValue='4,2,2,1', deserializer=TorpedoSpeeds.toTorpedoSpeed),
        KeyName(f'{GOOD_PLAYER}{KEY_NAME_SUFFIX}'):     ValueDescription(defaultValue='3,2,3,4', deserializer=TorpedoSpeeds.toTorpedoSpeed),
        KeyName(f'{EXPERT_PLAYER}{KEY_NAME_SUFFIX}'):   ValueDescription(defaultValue='2,2,4,4', deserializer=TorpedoSpeeds.toTorpedoSpeed),
        KeyName(f'{EMERITUS_PLAYER}{KEY_NAME_SUFFIX}'): ValueDescription(defaultValue='1,2,5,5', deserializer=TorpedoSpeeds.toTorpedoSpeed),
    }
)

SECTION_DEVELOPER: ValueDescriptions = ValueDescriptions(
    {
        KeyName('maxStarbaseSearches'):  ValueDescription(defaultValue='128', deserializer=SecureConversions.secureInteger),
        KeyName('maxCommanderSearches'): ValueDescription(defaultValue='128', deserializer=SecureConversions.secureInteger),
    }
)

# The schedule values should be set to True for normal game play
# A developer may choose to turn off those events for debug purposes
SECTION_DEBUG: ValueDescriptions = ValueDescriptions(
    {
        KeyName('manualPlaceShipInQuadrant'):                ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('manualSectorCoordinates'):                  ValueDescription(defaultValue='0,0',   deserializer=Coordinates.toCoordinates),
        KeyName('addKlingons'):                              ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('klingonCount'):                             ValueDescription(defaultValue='1',     deserializer=SecureConversions.secureInteger),
        KeyName('addCommanders'):                            ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('commanderCount'):                           ValueDescription(defaultValue='1',     deserializer=SecureConversions.secureInteger),
        KeyName('addSuperCommanders'):                       ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('superCommanderCount'):                      ValueDescription(defaultValue='1',     deserializer=SecureConversions.secureInteger),
        KeyName('printKlingonPlacement'):                    ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('addPlanet'):                                ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('addStarBase'):                              ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('noKlingons'):                               ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('noCommanders'):                             ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('noSuperCommanders'):                        ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('consoleShowInternals'):                     ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('scheduleSuperNova'):                        ValueDescription(defaultValue='True', deserializer=SecureConversions.secureBoolean),
        KeyName('scheduleTractorBeam'):                      ValueDescription(defaultValue='True', deserializer=SecureConversions.secureBoolean),
        KeyName('scheduleCommanderAttacksBase'):             ValueDescription(defaultValue='True', deserializer=SecureConversions.secureBoolean),
        KeyName('collectKlingonQuadrantCoordinates'):        ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('collectCommanderQuadrantCoordinates'):      ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('collectSuperCommanderQuadrantCoordinates'): ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('announceQuadrantCreation'):                 ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('debugBaseEnemyTorpedo'):                    ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('debugBaseEnemyTorpedoInterval'):            ValueDescription(defaultValue='20',    deserializer=SecureConversions.secureInteger),
        KeyName('debugSmoothMotion'):                        ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('debugSmoothMotionInterval'):                ValueDescription(defaultValue='5',     deserializer=SecureConversions.secureInteger),
        KeyName('drawSectionBoundaries'):                    ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('debugEvents'):                              ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
    }
)
GAME_SETTINGS_SECTIONS: Sections = Sections(
    {
        SectionName('Limits'):        SECTION_LIMITS,
        SectionName('Power'):         SECTION_POWER,
        SectionName('GameLevel'):     SECTION_GAME_LEVEL,
        SectionName('Factors'):       SECTION_FACTORS,
        SectionName('TorpedoSpeeds'): SECTION_SPEED_SETTINGS,
        SectionName('Developer'):     SECTION_DEVELOPER,
        SectionName('Debug'):         SECTION_DEBUG,
    }
)


class GameSettings(DynamicConfiguration, metaclass=SingletonV3):
    def __init__(self):

        self._logger: Logger = getLogger(__name__)

        super().__init__(baseFileName=GAME_SETTINGS_FILE_NAME, moduleName=APPLICATION_NAME, sections=GAME_SETTINGS_SECTIONS)
