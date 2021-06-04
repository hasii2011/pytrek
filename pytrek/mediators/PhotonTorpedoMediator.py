
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import Sprite
from arcade import SpriteList
from arcade import Texture
from arcade import check_for_collision_with_list
# from arcade import has_line_of_sight
from arcade import load_spritesheet

from pytrek.Constants import SOUND_VOLUME_HIGH

from pytrek.LocateResources import LocateResources
from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.Explosion import Explosion

from pytrek.gui.gamepieces.GamePieceTypes import Klingons
from pytrek.gui.gamepieces.Klingon import Klingon
from pytrek.gui.gamepieces.PhotonTorpedo import PhotonTorpedo
from pytrek.mediators.BaseMediator import BaseMediator
from pytrek.mediators.BaseMediator import LineOfSightResponse
from pytrek.model.Quadrant import Quadrant


class PhotonTorpedoMediator(BaseMediator):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)
        super().__init__()

        self._torpedoes:  SpriteList = SpriteList()
        self._explosions: SpriteList = SpriteList()

        self._loadSounds()

        self._torpedoTextures: List[Texture] = self._loadPhotonTorpedoExplosions()

    # noinspection PyUnusedLocal
    def draw(self, quadrant: Quadrant):
        self._torpedoes.draw()
        self._explosions.draw()

    # noinspection PyUnusedLocal
    def update(self, quadrant: Quadrant):
        self._torpedoes.update()
        self._explosions.update()

    def fireEnterpriseTorpedoesAtKlingons(self, quadrant: Quadrant):

        self._messageConsole.displayMessage("Firing Torpedoes!!")

        enterprise: Enterprise = quadrant.enterprise
        klingons:   Klingons   = quadrant.klingons

        if len(klingons) == 0:
            self._messageConsole.displayMessage("Don't waste torpedoes.  Nothing to fire at")
            self._noKlingonsSound.play(volume=SOUND_VOLUME_HIGH)
        else:
            startingPoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
            for klingon in klingons:
                endPoint: ArcadePoint = ArcadePoint(x=klingon.center_x, y=klingon.center_y)

                clearLineOfSight: LineOfSightResponse = self._doWeHaveLineOfSight(quadrant, startingPoint, endPoint)
                if clearLineOfSight.answer is True:
                    klingon: Klingon = cast(Klingon, klingon)
                    self._pointAtKlingon(enterprise=enterprise, klingon=klingon)
                    self._fireTorpedo(enterprise=enterprise, klingon=klingon)
                    self._photonTorpedoFired.play(volume=SOUND_VOLUME_HIGH)
                    self._gameState.torpedoCount -= 1
                else:
                    msg: str = (
                        f'Cannot fire at {klingon.id} '
                        f'because a {clearLineOfSight.obstacle.id} is in the way'
                    )
                    self._messageConsole.displayMessage(message=msg)
                    self.logger.info(msg)
            enterprise.angle = 0

    def handleTorpedoHits(self, quadrant: Quadrant):

        klingons:   Klingons  = quadrant.klingons
        enterprise: Enterprise = quadrant.enterprise
        for klingon in klingons:
            klingon: Klingon = cast(Klingon, klingon)
            if klingon.power > 0:
                expendedTorpedoes: List[Sprite] = check_for_collision_with_list(sprite=klingon, sprite_list=self._torpedoes)

                for killerTorpedo in expendedTorpedoes:
                    killerTorpedo: PhotonTorpedo = cast(PhotonTorpedo, killerTorpedo)
                    self.logger.info(f'{killerTorpedo.id} hit')

                    self.__doExplosion(killerTorpedo)

                    killerTorpedo.remove_from_sprite_lists()

                    self.__damageOrKillKlingon(enterprise, klingon)

        #
        # Remove Dead Klingons
        #
        quadrant.removeDeadKlingons()

    def _loadSounds(self):

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='photonTorpedo.wav')
        self._photonTorpedoFired: Sound = Sound(file_name=fqFileName)

        fqFileName = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME,
                                                      bareFileName='SmallExplosion.wav')
        self._explosionSound: Sound = Sound(file_name=fqFileName)

        fqFileName = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME,
                                                      bareFileName='inaccurateError.wav')
        self._noKlingonsSound: Sound = Sound(file_name=fqFileName)

    def _pointAtKlingon(self, klingon: Klingon, enterprise: Enterprise):

        currentPoint:     ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
        destinationPoint: ArcadePoint = ArcadePoint(x=klingon.center_x, y=klingon.center_y)

        normalAngle: float = self._computer.computeAngleToTarget(shooter=currentPoint, deadMeat=destinationPoint)
        enterprise.angle = normalAngle + 125

        self._messageConsole.displayMessage(f'Enterprise firing on course {enterprise.angle:.2f}')

    def _fireTorpedo(self, enterprise: Enterprise, klingon: Klingon):

        enterprisePoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
        klingonPoint:    ArcadePoint = ArcadePoint(x=klingon.center_x,    y=klingon.center_y)

        torpedo: PhotonTorpedo = PhotonTorpedo()

        torpedo.center_x = enterprisePoint.x
        torpedo.center_y = enterprisePoint.y
        torpedo.inMotion = True
        torpedo.firedAt  = klingon.id
        torpedo.destinationPoint = klingonPoint

        self._torpedoes.append(torpedo)
        self._messageConsole.displayMessage(f'Enterprise fire from: {enterprise.currentPosition} at Klingon {klingon.id}')

    def _loadPhotonTorpedoExplosions(self) -> List[Texture]:
        """
        Cache the torpedo explosion textures

        Returns:  The texture list
        """
        nColumns:  int = 8
        tileCount: int = 21
        spriteWidth:  int = 128
        spriteHeight: int = 128
        bareFileName: str = f'PhotonTorpedoExplosionSprites.png'
        fqFileName:   str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=bareFileName)

        explosions: List[Texture] = load_spritesheet(fqFileName, spriteWidth, spriteHeight, nColumns, tileCount)

        return explosions

    def _doWeHaveLineOfSight(self, quadrant: Quadrant, startingPoint: ArcadePoint, endPoint: ArcadePoint) -> LineOfSightResponse:
        """
        Check to see if planets, stars, other Klingons, Commanders, or StarBases prevent
        this klingon from shooting at the Enterprises

        Args:
            startingPoint:

        Returns:  `True` if no obstructions, else `False`
        """
        obstacles: SpriteList = SpriteList()
        if quadrant.hasPlanet is True:
            obstacles.append(quadrant._planet)

        # startTuple = (startingPoint.x, startingPoint.y)
        # endTuple   = (endPoint.x,      endPoint.y)
        # results = has_line_of_sight(point_1=startTuple, point_2=endTuple, walls=obstacles)

        results: LineOfSightResponse = self.hasLineOfSight(startingPoint=startingPoint, endPoint=endPoint, obstacles=obstacles)

        self.logger.info(f'{results=}')
        return results

    def __doExplosion(self, killerTorpedo: PhotonTorpedo):

        explosion: Explosion = Explosion(textureList=self._torpedoTextures, sound=self._explosionSound)
        explosion.center_x = killerTorpedo.center_x
        explosion.center_y = killerTorpedo.center_y

        self._explosions.append(explosion)

        self._explosionSound.play(SOUND_VOLUME_HIGH)

    def __damageOrKillKlingon(self, enterprise: Enterprise, klingon: Klingon):

        kHit: float = self._computer.computeHitValueOnKlingon(enterprisePosition=enterprise.currentPosition,
                                                              klingonPosition=klingon.currentPosition,
                                                              klingonPower=klingon.power)
        klingon.power -= kHit
        self._messageConsole.displayMessage(f'{klingon.id} took hit: {kHit:.2f}  remaining: {klingon.power:.2f}')
        if klingon.power <= 0:
            self._messageConsole.displayMessage(f'{klingon.id} destroyed')
            klingon.remove_from_sprite_lists()
            klingon.power = 0
