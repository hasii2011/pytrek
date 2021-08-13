
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import Sprite
from arcade import SpriteList
from arcade import load_spritesheet

from pytrek.GameState import GameState
from pytrek.LocateResources import LocateResources
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

        self._soundPhaser:         Sound = cast(Sound, None)
        self._soundUnableToComply: Sound = cast(Sound, None)

        self._loadSounds()

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

        enemies: Enemies = Enemies([])
        enemies.extend(quadrant.klingons)
        enemies.extend(quadrant.commanders)
        enemies.extend(quadrant.superCommanders)

        if len(enemies) == 0:
            self._soundUnableToComply.play(volume=self._gameSettings.soundVolume.value)
            self._messageConsole.displayMessage("Nothing to fire at")
        else:
            gameEngine: GameEngine = self._gameEngine
            enterpriseCoordinates: Coordinates = quadrant.enterpriseCoordinates

            self._gameState.energy -= phaserPower
            for enemy in enemies:
                distance: float = self._computer.computeQuadrantDistance(startSector=enterpriseCoordinates, endSector=enemy.gameCoordinates)

                hit:        float = gameEngine.doPhasers(distance=distance, enemyPower=enemy.power, powerAmount=phaserPower)
                enemyDrain: float = gameEngine.hitThem(distance=distance, hit=hit, enemyPower=enemy.power)

                enemy.power -= enemyDrain
                msg: str = f'Unit hit {enemyDrain:.2f} on {enemy.gameCoordinates} available: {enemy.power:.2f}'

                self._messageConsole.displayMessage(msg)
                self.logger.info(msg)

                self._placePhaserBolt(enterprise=quadrant.enterprise, enemy=enemy)
                self._soundPhaser.play(volume=self._gameSettings.soundVolume.value)
                if enemy.power <= 0.0:
                    deadMsg: str = f'Enemy at {enemy.gameCoordinates} dead'

                    self._messageConsole.displayMessage(deadMsg)
                    self.logger.info(deadMsg)
                    sprite: Sprite = cast(Sprite, enemy)
                    sprite.remove_from_sprite_lists()

    def _placePhaserBolt(self, enterprise: Enterprise, enemy: Enemy):

        start: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
        end:   ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)
        centerPoint: ArcadePoint = self._computer.computeCenterPoint(start=start, end=end)

        phaserBolt: PhaserBolt = PhaserBolt(textureList=self._phaserFireTextures)

        phaserBolt.center_x = centerPoint.x
        phaserBolt.center_y = centerPoint.y

        self._pointAtTarget(shooter=phaserBolt, target=enterprise, rotationAngle=180)

        self._phaserBolts.append(phaserBolt)

    def _loadSounds(self):
        self._soundPhaser         = self._loadSound('PhaserFire.wav')
        self._soundUnableToComply = self._loadSound(bareFileName='unableToComply.wav')

    def _loadSound(self, bareFileName: str) -> Sound:

        fqFileName: str = LocateResources.getResourcesPath(LocateResources.SOUND_RESOURCES_PACKAGE_NAME, bareFileName)
        sound: Sound = Sound(fqFileName)

        return sound

    def _loadFirePhaserTextures(self) -> TextureList:

        nColumns:  int = 3
        tileCount: int = 17
        spriteWidth:  int = 231
        spriteHeight: int = 134
        bareFileName: str = f'PhaserSpriteSheet.png'
        fqFileName:   str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=bareFileName)

        textureList: TextureList = cast(TextureList, load_spritesheet(fqFileName, spriteWidth, spriteHeight, nColumns, tileCount))

        return textureList
