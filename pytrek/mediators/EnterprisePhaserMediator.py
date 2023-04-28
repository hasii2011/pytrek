
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sprite
from arcade import SpriteList
from arcade import load_spritesheet

from pytrek.GameState import GameState

from pytrek.LocateResources import LocateResources
from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType
from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.GameEngine import GameEngine
from pytrek.gui.MessageConsole import MessageConsole
from pytrek.gui.gamepieces.Enterprise import Enterprise

from pytrek.gui.gamepieces.GamePieceTypes import Enemies
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.gui.gamepieces.PhaserBolt import PhaserBolt
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList

from pytrek.mediators.base.BaseMediator import BaseMediator
from pytrek.model.Coordinates import Coordinates

from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings


class EnterprisePhaserMediator(BaseMediator):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._gameSettings:   GameSettings   = GameSettings()
        self._gameEngine:     GameEngine     = GameEngine()
        self._gameState:      GameState      = GameState()
        self._messageConsole: MessageConsole = MessageConsole()
        self._soundMachine:   SoundMachine   = SoundMachine()

        self._phaserBolts: SpriteList = SpriteList()
        self._phaserFireTextures: TextureList = self._loadFirePhaserTextures()

    # noinspection PyUnusedLocal
    def draw(self, quadrant: Quadrant):
        self._phaserBolts.draw()

    # noinspection PyUnusedLocal
    def update(self, quadrant: Quadrant):
        self._phaserBolts.update()

    def phaserFireTextures(self) -> TextureList:
        return self._phaserFireTextures

    def firePhasers(self, quadrant: Quadrant, phaserPower: float = 300.0):
        """

        Args:
            quadrant:       The quadrant we are in
            phaserPower:    How much energy to expend

        """

        enemies: Enemies = Enemies([])
        enemies.extend(quadrant.klingons)
        enemies.extend(quadrant.commanders)
        enemies.extend(quadrant.superCommanders)

        if len(enemies) == 0:
            self._soundMachine.playSound(soundType=SoundType.UnableToComply)
            self._messageConsole.displayMessage("Nothing to fire at")
        else:
            enterpriseCoordinates: Coordinates = quadrant.enterpriseCoordinates

            self._gameState.energy -= phaserPower
            for enemy in enemies:
                self._damageEnemy(enemy, enterpriseCoordinates, phaserPower)

                self._placePhaserBolt(enterprise=quadrant.enterprise, enemy=enemy)
                self._soundMachine.playSound(soundType=SoundType.PhaserFired)
                if enemy.power <= 0.0:
                    self._killEnemy(quadrant=quadrant, enemy=enemy)

    def _placePhaserBolt(self, enterprise: Enterprise, enemy: Enemy):

        start: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
        end:   ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)
        centerPoint: ArcadePoint = self._computer.computeCenterPoint(start=start, end=end)

        phaserBolt: PhaserBolt = PhaserBolt(textureList=self._phaserFireTextures)

        phaserBolt.center_x = centerPoint.x
        phaserBolt.center_y = centerPoint.y

        self._pointAtTarget(shooter=phaserBolt, target=enterprise, rotationAngle=180)

        self._phaserBolts.append(phaserBolt)

    def _loadFirePhaserTextures(self) -> TextureList:

        nColumns:  int = 3
        tileCount: int = 17
        spriteWidth:  int = 231
        spriteHeight: int = 134
        bareFileName: str = f'PhaserSpriteSheet.png'
        fqFileName:   str = LocateResources.getImagePath(bareFileName=bareFileName)

        textureList: TextureList = cast(TextureList, load_spritesheet(fqFileName, spriteWidth, spriteHeight, nColumns, tileCount))

        return textureList

    def _damageEnemy(self, enemy: Enemy, enterpriseCoordinates: Coordinates, phaserPower: float):
        """
        Appropriately apply phaser damage to this agitator
        Args:
            enemy:      The subversive who is trying to demolish us
            enterpriseCoordinates:  Where the patriot is in the quadrant
            phaserPower:    How much to "jack" up the insurgent
        """

        gameEngine: GameEngine = self._gameEngine

        distance:   float = self._computer.computeQuadrantDistance(startSector=enterpriseCoordinates, endSector=enemy.gameCoordinates)
        hit:        float = gameEngine.doPhasers(distance=distance, enemyPower=enemy.power, powerAmount=phaserPower)
        enemyDrain: float = gameEngine.hitThem(distance=distance, hit=hit, enemyPower=enemy.power)

        enemy.power -= enemyDrain

        msg: str = f'Unit hit {enemyDrain:.2f} on {enemy.gameCoordinates} available: {enemy.power:.2f}'
        self._messageConsole.displayMessage(msg)
        self.logger.info(msg)

    def _killEnemy(self, quadrant: Quadrant, enemy: Enemy):
        """
        Remove enemy from board and update the game engine
        Args:
            enemy:  The "whacked" bad dude
        """

        deadMsg: str = f'Enemy at {enemy.gameCoordinates} destroyed'

        self._messageConsole.displayMessage(deadMsg)
        self.logger.info(deadMsg)
        self._gameEngine.decrementEnemyCount(enemy=enemy)
        quadrant.decrementEnemyCount(enemy=enemy)

        sprite: Sprite = cast(Sprite, enemy)
        sprite.remove_from_sprite_lists()
