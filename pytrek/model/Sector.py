
from typing import cast

from dataclasses import dataclass

from pytrek.gui.gamepieces.base.BaseGamePiece import BaseGamePiece
from pytrek.model.Coordinates import Coordinates
from pytrek.model.SectorType import SectorType


@dataclass
class Sector:

    sprite:      BaseGamePiece = cast(BaseGamePiece, None)
    type:        SectorType    = SectorType.EMPTY
    coordinates: Coordinates   = Coordinates(0, 0)

    def __str__(self) -> str:
        return f"SectorType: {str(self.type)}  Coordinates: {self.coordinates}"
