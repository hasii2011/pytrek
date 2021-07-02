
from logging import Logger
from logging import getLogger

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.BaseEnemy import BaseEnemy
from pytrek.gui.gamepieces.BaseEnemy import EnemyId
from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.model.Coordinates import Coordinates


class Commander(BaseEnemy):

    FILENAME: str = 'Commander.png'

    def __init__(self, coordinates: Coordinates, moveInterval: int):

        super().__init__(filename=Commander.FILENAME, coordinates=coordinates, moveInterval=moveInterval)

        self.logger: Logger = getLogger(__name__)

        self.id = EnemyId(f'Commander-{self.gameCoordinates}')

        # Compute at creation;  Mediator will move the commander
        arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(coordinates)

        self.center_x = arcadePoint.x
        self.center_y = arcadePoint.y

    def __str__(self):

        lookAtMe: str = f'{self.id}'

        return lookAtMe

    def __repr__(self):

        devMe: str = (
            f'Commander['
            f'id={self.id} '
            f'power={self.power:.3f} '
            f'moveInterval={self.moveInterval} '
            f'timeSinceMovement={self.timeSinceMovement} '
            f'currentPosition={self.gameCoordinates}'
            ']'
        )

        return devMe
