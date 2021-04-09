
from typing import cast

from dataclasses import dataclass

from gui.gamepieces.GamePiece import GamePiece
from pytrek.model.Coordinates import Coordinates
from pytrek.model.SectorType import SectorType


@dataclass
class Sector:

    sprite:      GamePiece   = cast(GamePiece, None)
    type:        SectorType  = SectorType.EMPTY
    coordinates: Coordinates = Coordinates(0, 0)

    def __str__(self) -> str:
        return f"SectorType: {str(self.type)}  Coordinates: {self.coordinates}"
