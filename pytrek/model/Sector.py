
from typing import cast
from dataclasses import field

from dataclasses import dataclass

from pytrek.gui.gamepieces.base.BaseGamePiece import BaseGamePiece

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Coordinates import coordinateFactory

from pytrek.model.SectorType import SectorType


@dataclass(repr=True)
class Sector:

    sprite:      BaseGamePiece = cast(BaseGamePiece, None)
    type:        SectorType    = SectorType.EMPTY
    coordinates: Coordinates   = field(default_factory=coordinateFactory)

    def __str__(self) -> str:
        return f"SectorType: {self.type}  Coordinates: {self.coordinates}"
