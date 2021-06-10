
from pytrek.gui.gamepieces.BaseEnemy import BaseEnemy
from pytrek.gui.gamepieces.BaseEnemy import EnemyId

from pytrek.model.Coordinates import Coordinates


class Klingon(BaseEnemy):

    FILENAME: str = 'KlingonD7.png'

    def __init__(self, coordinates: Coordinates):
        """

        Args:
            coordinates:   Current Game Position
        """
        super().__init__(filename=Klingon.FILENAME, coordinates=coordinates)

        self.id = EnemyId(f'Klingon-{self.gameCoordinates}')

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
