
from logging import Logger
from logging import getLogger
from typing import cast

from arcade import SpriteList

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.gui.gamepieces.BaseEnemy import EnemyId
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemies
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.mediators.BaseMediator import BaseMediator
from pytrek.mediators.BaseMediator import LineOfSightResponse

from pytrek.model.Quadrant import Quadrant


class BaseTorpedoMediator(BaseMediator):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self):

        super().__init__()

        self.logger: Logger = BaseTorpedoMediator.clsLogger

        self._torpedoes:        SpriteList = SpriteList()
        self._torpedoFollowers: SpriteList = SpriteList(is_static=True)
        self._misses:           SpriteList = SpriteList()

        self._klingonList:      Enemies = cast (Enemies, None)

        self._lastTimeCheck: float = self._gameEngine.gameClock / 1000
        self.logger.info(f'{self._lastTimeCheck=}')

    @property
    def torpedoes(self) -> SpriteList:
        return self._torpedoes

    @torpedoes.setter
    def torpedoes(self, newList: SpriteList):
        """
        Args:
            newList:
        """
        self._torpedoes = newList

    @property
    def torpedoFollowers(self) -> SpriteList:
        return self._torpedoFollowers

    @torpedoFollowers.setter
    def torpedoFollowers(self, newValues: SpriteList):
        self._torpedoFollowers = newValues

    @property
    def torpedoDuds(self) -> SpriteList:
        return self._misses

    @torpedoDuds.setter
    def torpedoDuds(self, newValues: SpriteList):
        self._misses = newValues

    def draw(self):
        """
        Implemented by subclass
        """
        pass

    def update(self, quadrant: Quadrant):
        """
        Implemented by subclass
        Args:
            quadrant:
        """
        pass

    def _fireTorpedoesAtEnterpriseIfNecessary(self, quadrant: Quadrant, enemies: Enemies):

        currentTime: float = self._gameEngine.gameClock

        # klingons: List[Klingon] = quadrant.klingons
        for enemy in enemies:
            deltaClockTime: float = currentTime - enemy.lastTimeCheck
            if deltaClockTime > enemy.firingInterval:
                self.logger.debug(f'Time for {enemy} to fire torpedoes')

                endPoint:            ArcadePoint = ArcadePoint(x=quadrant.enterprise.center_x, y=quadrant.enterprise.center_y)
                lineOfSightResponse: LineOfSightResponse = self._doWeHaveLineOfSight(quadrant, shooter=enemy, endPoint=endPoint)
                if lineOfSightResponse.answer is True:
                    self.__pointAtEnterprise(enemy=enemy, enterprise=quadrant.enterprise)
                    self._fireTorpedo(enemy=enemy, enterprise=quadrant.enterprise)
                else:
                    self._playCannotFireSound()
                    self._messageConsole.displayMessage(f'{enemy.id} cannot shoot, blocked by {lineOfSightResponse.obstacle.id}')

                enemy.lastTimeCheck = round(currentTime)

    def _fireTorpedo(self, enemy: Enemy, enterprise: Enterprise):
        """
        Implemented by subclass to fire the specific torpedo
        Args:
            enemy:      Who is firing it
            enterprise: The poor lowly enterprise is the target
        """
        pass

    def _playCannotFireSound(self):
        """
        Implemented by subclass
        """
        pass

    def _doWeHaveLineOfSight(self, quadrant: Quadrant, shooter: Enemy, endPoint: ArcadePoint) -> LineOfSightResponse:

        startingPoint: ArcadePoint = ArcadePoint(x=shooter.center_x, y=shooter.center_y)
        obstacles:     SpriteList  = SpriteList()

        if quadrant.hasPlanet is True:
            obstacles.append(quadrant.planet)

        otherEnemies: Enemies = self.__buildEligibleEnemyObstacles(shooter=shooter, enemies=quadrant.klingons)

        obstacles.extend(otherEnemies)

        results: LineOfSightResponse = self._hasLineOfSight(startingPoint=startingPoint, endPoint=endPoint, obstacles=obstacles)

        self.logger.debug(f'{results=}')
        return results

    def _findFiringEnemy(self, enemyId: EnemyId, enemies: Enemies) -> Enemy:
        """

        Args:
            enemyId:    The ID of the enemy that fired
            enemies:    The list we are searching

        Returns:  May return 'None' if the Enterprise killed him
        """

        fndEnemy: Enemy = cast(Enemy, None)
        for enemy in enemies:
            # enemy: Enemy = cast(Enemy, enemy)
            if enemy.id == enemyId:
                fndEnemy = enemy
                break

        return fndEnemy

    def __pointAtEnterprise(self, enemy: Enemy, enterprise: Enterprise):

        currentPoint:     ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)
        destinationPoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)

        normalAngle: float = self._computer.computeAngleToTarget(shooter=currentPoint, deadMeat=destinationPoint)
        enemy.angle = normalAngle + 125

        self.logger.debug(f'{enemy.angle=}')

    def __buildEligibleEnemyObstacles(self, shooter: Enemy, enemies: Enemies) -> Enemies:
        """

        Returns:  A list of enemies excluding the shooter
        """
        obstacles: Enemies = Enemies([])
        for enemy in enemies:
            if enemy.id != shooter.id:
                obstacles.append(enemy)
        return obstacles
