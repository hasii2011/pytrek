
from typing import cast
from dataclasses import field

from dataclasses import dataclass

from src.pytrek.gui.gamepieces.base.BaseGamePiece import BaseGamePiece

from src.pytrek.model.Coordinates import Coordinates
from src.pytrek.model.Coordinates import coordinateFactory

from src.pytrek.model.SectorType import SectorType


@dataclass(repr=True)
class Sector:

    sprite:      BaseGamePiece = cast(BaseGamePiece, None)
    type:        SectorType    = SectorType.EMPTY
    coordinates: Coordinates   = field(default_factory=coordinateFactory)

    def __str__(self) -> str:
        return f"SectorType: {self.type}  Coordinates: {self.coordinates}"
