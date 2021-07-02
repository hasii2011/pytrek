from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.gui.gamepieces.base.BaseEnemy import BaseEnemy
from pytrek.gui.gamepieces.base.BaseEnemy import EnemyId
from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.model.Coordinates import Coordinates


class Klingon(BaseEnemy):

    FILENAME: str = 'KlingonD7.png'

    def __init__(self, coordinates: Coordinates, moveInterval: int = 0):
        """

        Args:
            coordinates:   Current Game Position
            moveInterval:  Only set at advanced game levels
        """
        super().__init__(filename=Klingon.FILENAME, coordinates=coordinates)

        self.id           = EnemyId(f'Klingon-{self.gameCoordinates}')
        self.moveInterval = moveInterval
        # Compute at creation;  Mediator will move the Klingon at advance game conditions
        arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(coordinates)

        self.center_x = arcadePoint.x
        self.center_y = arcadePoint.y

    def __str__(self):

        lookAtMe: str = f'{self.id=}'
        return lookAtMe

    def __repr__(self):

        devMe: str = (
            f'Klingon['
            f'{self.id=} '
            f'power={self.power:.3f} '
            f'firingInterval={self.firingInterval} '
            f'{self.gameCoordinates=}'
            ']'
        )

        return devMe
