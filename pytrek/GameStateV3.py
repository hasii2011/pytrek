
from typing import AnyStr
from typing import Type
from typing import Union

from enum import Enum

from pathlib import Path

from dataclasses import dataclass


from dataclass_wizard import DumpMixin
from dataclass_wizard import JSONSerializable
from dataclass_wizard import LoadMixin
from dataclass_wizard.type_def import E
from dataclass_wizard.type_def import N

from pytrek.ConfigurationLocator import ConfigurationLocator

from pytrek.Constants import APPLICATION_NAME

from pytrek.model.Coordinates import Coordinates

from pytrek.engine.GameType import GameType

from pytrek.engine.PlayerType import PlayerType
from pytrek.engine.ShipCondition import ShipCondition


JSON_FILENAME: str = 'GameStateV3.json'


@dataclass
class GameStateV3(JSONSerializable, LoadMixin, DumpMixin):
    """
    This is a Frankenstein data class that
        * Is a singleton
        * self loads JSON
        * self saves JSON
        * Initialize a default game

    """

    _instance = None

    gameActive:                 bool  = True
    energy:                     float = 0.0
    shieldEnergy:               float = 0.0
    inTime:                     float = 0.0
    opTime:                     float = 0.0
    starDate:                   float = 0.0
    remainingGameTime:          float = 0.0
    remainingKlingons:          int = 0
    remainingCommanders:        int = 0
    remainingSuperCommanders:   int = 0
    torpedoCount:               int = 0
    starBaseCount:              int = 0
    planetCount:                int = 0

    currentQuadrantCoordinates: Coordinates = Coordinates(0, 0)
    currentSectorCoordinates:   Coordinates = Coordinates(0, 0)

    shipCondition:      ShipCondition = ShipCondition.Green
    playerType:         PlayerType    = PlayerType.Good
    gameType:           GameType      = GameType.Medium

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GameStateV3, cls).__new__(cls, *args, **kwargs)
            # Initialize your configuration settings here
        return cls._instance

    def restore(self)  -> 'GameStateV3':

        with open(self._filePath(), 'r') as fd:
            jsonStr: str = fd.read()

        return self.from_json(jsonStr)

    def save(self):
        with open(self._filePath(), 'w') as fd:
            fd.write(self.to_json(indent=4))

    @staticmethod
    def dump_with_enum(o: E, *_):
        """
        Override persist values, we persist names of enumerations
        """
        return o.name

    @staticmethod
    def load_to_enum(o: Union[AnyStr, N], base_type: Type[Enum]) -> Enum:
        """
        Get our custom saved enumeration; Human readable
        """
        ans = base_type[o]      # type: ignore
        return ans

    def resetStatistics(self):
        self.gameActive = True

    def _filePath(self) -> Path:

        configurationLocator: ConfigurationLocator = ConfigurationLocator()

        appPath: Path = configurationLocator.applicationPath(APPLICATION_NAME)
        if appPath.exists() is False:
            appPath.mkdir(exist_ok=True)
        fqPath:  Path = appPath / JSON_FILENAME

        return fqPath

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} at {hex(id(self))}>'
