
from logging import Logger
from logging import getLogger
from logging import INFO

from random import randrange
from random import random

from pytrek.Constants import GALAXY_COLUMNS
from pytrek.Constants import GALAXY_ROWS
from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS

from pytrek.Singleton import Singleton

from pytrek.model.Coordinates import Coordinates

from pytrek.settings.GameSettings import GameSettings


class Intelligence(Singleton):
    """
    This is a smart piece of code
    """

    RAND_MAX: int = 32767

    def init(self):
        """
        """
        self.logger:  Logger = getLogger(__name__)

        self._gameSettings: GameSettings = GameSettings()

    def generateSectorCoordinates(self) -> Coordinates:
        """
        Generate a random set of sector coordinates
        """
        x = randrange(QUADRANT_COLUMNS)
        y = randrange(QUADRANT_ROWS)

        return Coordinates(x=x, y=y)

    def generateQuadrantCoordinates(self) -> Coordinates:
        """
        Generate a random set of quadrant coordinates
        """
        x = randrange(GALAXY_COLUMNS)
        y = randrange(GALAXY_ROWS)

        return Coordinates(x, y)

    def generateInitialGameTime(self) -> float:
        """"""
        if self.logger.level == INFO:
            msg = (
                f"Game Length factor: '{self._gameSettings.gameLengthFactor}' "
                f"GameType: '{self._gameSettings.gameType}' "
                f" GameTypeValue: '{self._gameSettings.gameType.value}'"
            )
            self.logger.info(msg)
        remainingGameTime = self._gameSettings.gameLengthFactor * self._gameSettings.gameType.value
        return remainingGameTime

    def generateInitialKlingonCount(self, remainingGameTime: float) -> int:
        """
        ```
        private double dremkl = 2.0*intime*((skill+1 - 2*Intelligence.Rand())*skill*0.1+0.15);

        public int myRemainingKlingons = (int) Math.round(dremkl);
        self.remainingKlingons = ((2.0 * self.remainingGameTime) * (self.skill.value + 1)) - (2 * nextNum) * (self.skill.value * 0.1) + 0.15
        ```
        """
        nextNum = random() / 4.0
        self.logger.info(f"Random value: {nextNum:.4f}")

        self.remainingKlingons = (remainingGameTime * nextNum) + self._gameSettings.playerType.value + self._gameSettings.gameType.value
        self.remainingKlingons = round(self.remainingKlingons)

        if self.logger.level == INFO:
            message = (
                f"PlayerType: '{self._gameSettings.playerType} "
                f"GameType '{self._gameSettings.gameType}' "
                f"klingonCount: '{str(self.remainingKlingons)}'"
            )
            self.logger.info(message)

        return self.remainingKlingons

    def generateInitialStarDate(self) -> int:

        starDate: int = int(100.0 * (31.0 * random()) * 20.0)
        return starDate

    def computeKlingonPower(self) -> float:
        """
        Regular klingon
            kpower[i] = Rand()*150.0 +300.0 +25.0*skill;

        Returns:

        """
        kPower: float = (self.rand() * 150.0) + 300.0 + (25.0 * self._gameSettings.playerType.value)
        return kPower

    def rand(self) -> float:
        """

        double Rand(void) {
            return rand()/(1.0 + (double)RAND_MAX);
        }

        Returns: Random float in range 0.0 - 0.99999

        """
        intermediateAns = randrange(start=0, stop=Intelligence.RAND_MAX)
        ans: float = intermediateAns / (1.0 + Intelligence.RAND_MAX)

        return ans
