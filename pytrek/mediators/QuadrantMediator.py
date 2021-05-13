from typing import List
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG
from uuid import uuid4

from arcade import Sound
from arcade import Sprite
from arcade import SpriteList
from arcade import check_for_collision_with_list

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS
from pytrek.Constants import SOUND_VOLUME_HIGH

from pytrek.LocateResources import LocateResources

from pytrek.engine.Computer import Computer
from pytrek.engine.ArcadePosition import ArcadePosition
from pytrek.engine.GameEngine import GameEngine

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import KlingonId
from pytrek.gui.gamepieces.Klingon import Klingon
from pytrek.gui.gamepieces.KlingonTorpedo import KlingonTorpedo
from pytrek.gui.gamepieces.KlingonTorpedoFollower import KlingonTorpedoFollower

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.Singleton import Singleton


class QuadrantMediator(Singleton):
    """
    This class avoids putting UI logic (arcade) in the model class, Quadrant.
    """

    KLINGON_TORPEDO_EVENT_SECONDS = 10      # TODO  Compute this

    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        self._gameEngine: GameEngine = GameEngine()
        self._computer:   Computer   = Computer()

        self._playerList:    SpriteList = SpriteList()
        self._klingonList:   SpriteList = SpriteList()
        self._commanderList: SpriteList = SpriteList()

        self._klingonTorpedoes: SpriteList = cast(SpriteList, None)
        self._torpedoFollowers: SpriteList = cast(SpriteList, None)

        self._soundKlingonTorpedo: Sound = cast(Sound, None)
        fqFileName = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME,
                                                      bareFileName='klingon_torpedo.wav')
        self._soundKlingonTorpedo = Sound(file_name=fqFileName)

        self._lastTimeCheck: float = self._gameEngine.gameClock / 1000
        self.logger.info(f'{self._lastTimeCheck=}')

    @property
    def playerList(self) -> SpriteList:
        return self._playerList

    @playerList.setter
    def playerList(self, newValues: SpriteList):
        self._playerList = newValues

    @property
    def klingonList(self) -> SpriteList:
        return self._klingonList

    @klingonList.setter
    def klingonList(self, newValues: SpriteList):
        self._klingonList = newValues

    @property
    def commanderList(self) -> SpriteList:
        return self._commanderList

    @commanderList.setter
    def commanderList(self, newValues: SpriteList):
        self._commanderList = newValues

    @property
    def klingonTorpedoes(self) -> SpriteList:
        return self._klingonTorpedoes

    @klingonTorpedoes.setter
    def klingonTorpedoes(self, newList: SpriteList):
        """
        Args:
            newList:
        """
        self._klingonTorpedoes = newList

    @property
    def torpedoFollowers(self) -> SpriteList:
        return self._torpedoFollowers

    @torpedoFollowers.setter
    def torpedoFollowers(self, newValues: SpriteList):
        self._torpedoFollowers = newValues

    def update(self, quadrant: Quadrant):

        if self.logger.getEffectiveLevel() == DEBUG:
            self.logger.debug(f'{quadrant.enterpriseCoordinates=}')
            if quadrant.klingonCount > 0:
                self.logger.debug(f'{quadrant.klingonCount=}')

        self._updateQuadrant(quadrant)

        currentTime:    float = self._gameEngine.gameClock
        deltaClockTime: float = currentTime - self._lastTimeCheck
        if deltaClockTime > QuadrantMediator.KLINGON_TORPEDO_EVENT_SECONDS:
            self.logger.info(f'Time for Klingons to fire torpedoes')
            klingons: List[Klingon] = quadrant.klingons
            for klingon in klingons:
                self._fireKlingonTorpedo(klingon=klingon, enterprise=quadrant.enterprise)

            self._lastTimeCheck = currentTime

        self.playerList.update()
        self.klingonTorpedoes.update()
        self.torpedoFollowers.update()

        self._handleKlingonTorpedoHits(quadrant)
        #
        # TODO: Account for torpedo missing when Enterprise moves
        #

    def _handleKlingonTorpedoHits(self, quadrant: Quadrant):
        """
        Uses arcade to determine collision;  For each torpedo that hit

         * Remove it's followers
         * Determine which Klingon fired it
         * Determine how severe of a hit it was
         * Adjust the Enterprise shield power value or the Enterprise power value itself
        Args:
            quadrant:  The current quadrant we are in
        """

        expendedTorpedoes: List[Sprite] = check_for_collision_with_list(sprite=quadrant.enterprise, sprite_list=self.klingonTorpedoes)
        for expendedTorpedo in expendedTorpedoes:
            expendedTorpedo: KlingonTorpedo = cast(KlingonTorpedo, expendedTorpedo)
            self.logger.info(f'{expendedTorpedo.uuid} arrived at destination')
            self._removeTorpedoFollowers(klingonTorpedo=expendedTorpedo)

            firedBy: KlingonId = expendedTorpedo.firedBy
            shootingKlingon: Klingon = self._findFiringKlingon(uuid=firedBy)

            hitValue: float = self._computer.computeHitValueOnEnterprise(klingonPosition=shootingKlingon.currentPosition,
                                                                         enterprisePosition=quadrant.enterpriseCoordinates,
                                                                         klingonPower=shootingKlingon.power)
            self.logger.info(f'*** Enterprise was hit ***  {hitValue=} {shootingKlingon}')

            expendedTorpedo.remove_from_sprite_lists()

    def _updateQuadrant(self, quadrant):
        for y in range(QUADRANT_ROWS):
            for x in range(QUADRANT_COLUMNS):

                sector: Sector = quadrant.getSector(Coordinates(x, y))
                self.logger.debug(f'{sector}')

                gamePiece: GamePiece = sector.sprite
                sectorType: SectorType = sector.type

                if sectorType != SectorType.EMPTY:
                    if sectorType == SectorType.ENTERPRISE:
                        self._updateEnterprise(quadrant=quadrant, gamePiece=gamePiece)
                    elif sectorType == SectorType.KLINGON:
                        self._updateKlingon(gamePiece=gamePiece)

    def _updateEnterprise(self, quadrant: Quadrant, gamePiece: GamePiece):
        """
        Updates the Enterprise.  Account for in motion or stationary

        Args:
            quadrant:  The inspected quadrant
            gamePiece: The game piece found in the quadrant
        """
        enterprise: Enterprise = cast(Enterprise, gamePiece)
        arcadeX, arcadeY = GamePiece.gamePositionToScreenPosition(quadrant.enterpriseCoordinates)
        if enterprise.inMotion is True:

            self.logger.debug(f'Enterprise arcade position: ({arcadeX},{arcadeY})')
            enterprise.destinationPoint = ArcadePosition(x=arcadeX, y=arcadeY)
            enterprise.update()
        else:
            enterprise.center_x = arcadeX
            enterprise.center_y = arcadeY

    def _updateKlingon(self, gamePiece: GamePiece):

        klingon: Klingon = cast(Klingon, gamePiece)

        arcadeX, arcadeY = GamePiece.gamePositionToScreenPosition(klingon.currentPosition)

        klingon.center_x = arcadeX
        klingon.center_y = arcadeY

    def _fireKlingonTorpedo(self, klingon: Klingon, enterprise: Enterprise):

        self.logger.info(f'Klingon @ {klingon.currentPosition} firing; Enterprise @ {enterprise.currentPosition}')

        #
        # Use the enterprise arcade position rather than compute the sector center;  That way we
        # can use Arcade collision detection
        #
        klingonPoint:    ArcadePosition = Computer.gamePositionToScreenPosition(gameCoordinates=klingon.currentPosition)
        enterprisePoint: ArcadePosition = ArcadePosition(x=enterprise.center_x, y=enterprise.center_y)

        klingonTorpedo: KlingonTorpedo = KlingonTorpedo()
        klingonTorpedo.center_x = klingonPoint.x
        klingonTorpedo.center_y = klingonPoint.y
        klingonTorpedo.inMotion = True
        klingonTorpedo.destinationPoint  = enterprisePoint
        klingonTorpedo.firedFromPosition = klingon.currentPosition
        klingonTorpedo.firedBy           = klingon.id
        klingonTorpedo.followers         = self.torpedoFollowers

        self.klingonTorpedoes.append(klingonTorpedo)
        self._soundKlingonTorpedo.play(volume=SOUND_VOLUME_HIGH)
        self.logger.info(f'{klingonTorpedo.firedFromPosition=}')

    def _removeTorpedoFollowers(self, klingonTorpedo: KlingonTorpedo):

        followersToRemove: List[Sprite] = []
        for follower in self.torpedoFollowers:
            follower: KlingonTorpedoFollower = cast(KlingonTorpedoFollower, follower)
            if follower.following == klingonTorpedo.uuid:
                self.logger.debug(f'Removing follower: {follower.uuid}')
                followersToRemove.append(follower)

        for followerToRemove in followersToRemove:
            followerToRemove.remove_from_sprite_lists()

    def _findFiringKlingon(self, uuid: uuid4) -> Klingon:

        fndKlingon: Klingon = cast(Klingon, None)
        for klingon in self._klingonList:
            klingon: Klingon = cast(Klingon, klingon)
            if klingon.id == uuid:
                fndKlingon = klingon
                break

        return fndKlingon
