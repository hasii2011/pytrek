
from pytrek.gui.gamepieces.BaseEnemy import BaseEnemy

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.mediators.BaseMediator import BaseMediator


class BaseEnemyMediator(BaseMediator):

    def __init__(self):
        super().__init__()

    def _enemyMovedUpdateQuadrant(self, quadrant: Quadrant, enemy: BaseEnemy, newPosition: Coordinates, oldPosition: Coordinates):

        oldSector: Sector = quadrant.getSector(sectorCoordinates=oldPosition)

        oldSector.type   = SectorType.EMPTY
        oldSector.sprite = None

        newSector: Sector = quadrant.getSector(sectorCoordinates=newPosition)

        newSector.type   = SectorType.COMMANDER
        newSector.sprite = enemy
