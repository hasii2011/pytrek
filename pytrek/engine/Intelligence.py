from math import log
from typing import List

from logging import Logger
from logging import getLogger
from logging import INFO

from random import randint
from random import randrange
from random import random
from random import choice

from pytrek.Constants import GALAXY_COLUMNS
from pytrek.Constants import GALAXY_ROWS
from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS

from pytrek.engine.Direction import Direction
from pytrek.engine.GameType import GameType
from pytrek.engine.LRScanCoordinates import LRScanCoordinates
from pytrek.engine.PlayerType import PlayerType

from pytrek.gui.gamepieces.PlanetType import PlanetType

from pytrek.model.Coordinates import Coordinates
from pytrek.model.DataTypes import LRScanCoordinatesList

from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds

from pytrek.Singleton import Singleton


class Intelligence(Singleton):
    """
    This is a smart piece of code
    """

    RAND_MAX: int = 32767

    ADJACENT_DIRECTIONS: List[Direction] = [
        Direction.North, Direction.NorthEast, Direction.East
    ]

    def init(self):
        """
        """
        self.logger:        Logger       = getLogger(__name__)
        self._gameSettings: GameSettings = GameSettings()

    def getTorpedoSpeeds(self, playerType: PlayerType) -> TorpedoSpeeds:
        """
        Get the TorpedoSpeeds based on the player type
        Args:
            playerType:  What is the player's professed skill level?

        Returns:  The appropriate torpedo speed object
        """
        if playerType == PlayerType.Novice:
            retSpeed: TorpedoSpeeds = self._gameSettings.noviceTorpedoSpeeds
        elif playerType == PlayerType.Fair:
            retSpeed = self._gameSettings.fairTorpedoSpeeds
        elif playerType == PlayerType.Good:
            retSpeed = self._gameSettings.goodTorpedoSpeeds
        elif playerType == PlayerType.Expert:
            retSpeed = self._gameSettings.expertTorpedoSpeeds
        elif playerType == PlayerType.Emeritus:
            retSpeed = self._gameSettings.emeritusTorpedoSpeeds
        else:
            raise ValueError('Unknown Player Type')

        return retSpeed

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

    # noinspection SpellCheckingInspection
    def generateInitialKlingonCount(self, gameType: GameType, playerType: PlayerType) -> int:
        """
        ```
        private double dremkl = 2.0*intime*((skill+1 - 2*Intelligence.Rand())*skill*0.1+0.15);

        public int myRemainingKlingons = (int) Math.round(dremkl);
        self.remainingKlingons = ((2.0 * self.remainingGameTime) * (self.skill.value + 1)) - (2 * nextNum) * (self.skill.value * 0.1) + 0.15
        ```
        // Determine the initial values of klingons.
        // Values are different for Wglxy variation because the small variation option
        // is usually set. That narrows the range low-high of k counts.

        game.state.remtime = 7.0 * game.length;
        game.intime = game.state.remtime;

        int rFactor = 2;
        double mOffset = 0.15d;
        if ((game.options & OPTION_SMALL_VARIANCE_IN_K) != 0) {
           rFactor = 1;
           mOffset = 0.20d;
        }
        game.state.nscrem = game.inscom = (game.skill > SKILL_FAIR ? 1 : 0);
        game.state.remkl = game.inkling = (int) Math.round (2.0*game.intime
                                                   * (game.skill+1 - rFactor*tk.rand ())
                                                   * game.skill*0.1 + mOffset);
        """

        rFactor: int   = 2
        mOffset: float = 0.20
        skill:   int   = playerType.value
        remTime: float = 7.0 * gameType.value

        remainingKlingons: float = 2.0 * remTime * (skill + 1 - rFactor * self.rand()) * skill * 0.1 + mOffset

        remainingKlingons = round(remainingKlingons)

        if self.logger.level == INFO:
            message = (
                f"PlayerType: '{playerType} "
                f"GameType '{gameType}' "
                f"klingonCount: '{str(remainingKlingons)}'"
            )
            self.logger.info(message)

        return int(remainingKlingons)

    # noinspection SpellCheckingInspection
    def generateInitialCommanderCount(self, playerType: PlayerType, generatedKlingons: int) -> int:
        """
        incom = skill + 0.0625*inkling*Rand();

        Returns:  Klingon Commander Count
        """
        commanderCount = playerType.value * 0.0625 * generatedKlingons * self.rand()
        commanderCount = round(commanderCount)

        return commanderCount

    def generateInitialSuperCommanderCount(self, playerType: PlayerType, numberOfKlingons: int):
        """
        We will generate no more than
        * 1 super commander per 10 Klingons (Novice, Fair, Good)
        * 1 super commander per 5 Klingons (Expert)
        * 1 super commander per 3 Klingons (Emeritus)

        Args:
            playerType:         We need the skill level
            numberOfKlingons:  The current number of Klingons


        Returns An appropriate number for generating Super Commanders:
        """
        if playerType == PlayerType.Novice or playerType == PlayerType.Fair or playerType == PlayerType.Good:
            nSCount: int = numberOfKlingons // 10
        elif playerType == PlayerType.Expert:
            nSCount = numberOfKlingons // 5
        elif playerType == PlayerType.Emeritus:
            nSCount = numberOfKlingons // 3
        else:
            raise ValueError('Unknown Player Type')

        return nSCount

    def generateInitialStarDate(self) -> int:
        # noinspection SpellCheckingInspection
        """
        d.date = indate = 100.0*(int)(31.0*Rand()+20.0);

        Returns:  A start star date
        """

        starDate: int = int(100.0 * (31.0 * random()) * 20.0)
        return starDate

    def generateInitialStarBaseCount(self) -> int:
        # noinspection SpellCheckingInspection
        """
        Calculate and returns the star base count for the game start
        With the default values guarantees a minimum of 2 and a maximum of 5

        ```c
        d.rembase = 3.0*Rand()+2.0;
        ```

        Returns:    A StarBase count
        """
        multiplier: float = self._gameSettings.starBaseMultiplier
        extender:   float = self._gameSettings.starBaseExtender
        # double rb = (3.0 * ourGPRandomGenerator.nextDouble()) + 2.0;
        nextDouble = random()
        self.logger.debug("nextDouble: %s", str(nextDouble))

        retBaseCount: float = (multiplier * nextDouble) + extender

        retBaseCount = round(retBaseCount)
        self.logger.info("calculated retBaseCount: %s", str(retBaseCount))

        minimumStarBases: int = self._gameSettings.minimumStarBases
        maximumStarBases: int = self._gameSettings.maximumStarBases

        if retBaseCount < minimumStarBases:
            retBaseCount = minimumStarBases
            self.logger.info(f"adjusted retBaseCount: %s", str(retBaseCount))
        elif retBaseCount > maximumStarBases:
            retBaseCount = maximumStarBases
            self.logger.info(f"adjusted retBaseCount: %s", str(retBaseCount))

        return int(retBaseCount)

    def generateAdjacentCoordinates(self, centerCoordinates: Coordinates) -> LRScanCoordinatesList:

        coordinatesList: LRScanCoordinatesList = LRScanCoordinatesList([])

        for direction in Direction:
            self.logger.debug(f'{direction}')
            newCoordinates: Coordinates = centerCoordinates.newCoordinates(direction)
            if newCoordinates.valid() is True:

                lrScanCoordinates: LRScanCoordinates = LRScanCoordinates()
                lrScanCoordinates.coordinates = newCoordinates
                lrScanCoordinates.direction   = direction

                coordinatesList.append(lrScanCoordinates)

        return coordinatesList

    # noinspection SpellCheckingInspection
    def computeKlingonPower(self) -> float:
        """
        Regular klingon
            kpower[i] = Rand()*150.0 +300.0 +25.0*skill;

        Returns:

        """
        kPower: float = (self.rand() * 150.0) + 300.0 + (25.0 * self._gameSettings.playerType.value)
        return kPower

    # noinspection SpellCheckingInspection
    def computeCommanderPower(self, playerType: PlayerType) -> float:
        """

        Commander
            kpower[klhere] = 950.0+400.0*Rand()+50.0*skill;

        Returns:

        """
        cPower: float = 950.0 + (400.0 * self.rand()) + (50.0 * playerType.value)
        return cPower

    # noinspection SpellCheckingInspection
    def computeSuperCommanderPower(self, playerType: PlayerType) -> float:
        """

        Super Commander
            kpower[1] = 1175.0 + 400.0*Rand() + 125.0*skill;

        Returns:
        """
        scPower: float = 1175.0 + (400.0 * self.rand()) + (50.0 * playerType.value)
        return scPower

    def computeKlingonFiringInterval(self) -> int:
        """
        Klingons fire at different intervals;  Randomly compute something between the
        MIN_KLINGON_FIRING_INTERVAL and the MAX_KLINGON_FIRING_INTERVAL

        Returns: A random time interval
        """
        minFiringInterval: int = self._gameSettings.minKlingonFiringInterval
        maxFiringInterval: int = self._gameSettings.maxKlingonFiringInterval

        return randint(minFiringInterval, maxFiringInterval)

    def computeCommanderFiringInterval(self) -> int:
        minFiringInterval: int = self._gameSettings.minCommanderFiringInterval
        maxFiringInterval: int = self._gameSettings.maxCommanderFiringInterval

        return randint(minFiringInterval, maxFiringInterval)

    def computeSuperCommanderFiringInterval(self) -> int:
        minFiringInterval: int = self._gameSettings.minSuperCommanderFiringInterval
        maxFiringInterval: int = self._gameSettings.maxSuperCommanderFiringInterval

        return randint(minFiringInterval, maxFiringInterval)

    def computeSuperCommanderMoveInterval(self) -> int:
        minMoveInterval: int = self._gameSettings.minSuperCommanderMoveInterval
        maxMoveInterval: int = self._gameSettings.maxSuperCommanderMoveInterval

        return randint(minMoveInterval, maxMoveInterval)

    def computeCommanderMoveInterval(self) -> int:
        minMoveInterval: int = self._gameSettings.minCommanderMoveInterval
        maxMoveInterval: int = self._gameSettings.maxCommanderMoveInterval

        return randint(minMoveInterval, maxMoveInterval)

    def computeKlingonMoveInterval(self) -> int:
        minMoveInterval: int = self._gameSettings.minKlingonMoveInterval
        maxMoveInterval: int = self._gameSettings.maxKlingonMoveInterval

        return randint(minMoveInterval, maxMoveInterval)

    def computePlanetsInGalaxy(self) -> int:
        # noinspection SpellCheckingInspection
        """
        Will some times generate 1 more than maximumPlanets;  Hence my patch
        ```C
            nplan = (PLNETMAX/2) + (PLNETMAX/2+1)*Rand();
        ```
        Returns:  The planets to position in the Galaxy
        """
        maxPlanets:  int = self._gameSettings.maximumPlanets

        rb: float = (maxPlanets/2) + (maxPlanets/2 + 1) * self.randomFloat()

        planetCount: int = round(rb)
        if planetCount >= maxPlanets:
            planetCount = maxPlanets
        return planetCount

    def computeRandomPlanetType(self) -> PlanetType:

        planetTypeList = [name for name in dir(PlanetType) if not name.startswith('_')]

        planetName: str = choice(planetTypeList)

        return PlanetType(planetName)

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

    def randomFloat(self) -> float:
        """

        Returns:  0.0 .. 0.9999

        """

        weeNumber: float = random()
        return weeNumber

    def square(self, num: float):
        """
        Emulates sst square()

            double square(double i) { return i*i; }

        Args:
            num:  The number to square

        Returns:  The input number squared
        """
        return num * num

    def exponentialRandom(self, average: float) -> float:
        # noinspection SpellCheckingInspection
        """

        1e-7 -- 1 × 10 (minus 5) or 0.0000001
        double expran(double avrage) {
            return -avrage * log(1e-7 + Rand());
        }
        Returns:
        """
        return -average * log(1e-7 + self.rand())
