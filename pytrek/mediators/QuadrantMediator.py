
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG

from arcade import MOUSE_BUTTON_RIGHT
from arcade import Sound
from arcade import SpriteList

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS
from pytrek.GameState import GameState

from pytrek.engine.Computer import Computer
from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.ShipCondition import ShipCondition
from pytrek.gui.MessageConsole import MessageConsole

from pytrek.gui.gamepieces.commander.Commander import Commander
from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.gui.gamepieces.klingon.Klingon import Klingon
from pytrek.gui.gamepieces.supercommander.SuperCommander import SuperCommander

from pytrek.mediators.CommanderMediator import CommanderMediator
from pytrek.mediators.CommanderTorpedoMediator import CommanderTorpedoMediator
from pytrek.mediators.EnterpriseMediator import EnterpriseMediator
from pytrek.mediators.EnterprisePhaserMediator import EnterprisePhaserMediator
from pytrek.mediators.KlingonMediator import KlingonMediator
from pytrek.mediators.KlingonTorpedoMediator import KlingonTorpedoMediator
from pytrek.mediators.EnterpriseTorpedoMediator import EnterpriseTorpedoMediator
from pytrek.mediators.SuperCommanderMediator import SuperCommanderMediator
from pytrek.mediators.SuperCommanderTorpedoMediator import SuperCommanderTorpedoMediator
from pytrek.mediators.base.BaseMediator import BaseMediator

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.Singleton import Singleton
from pytrek.settings.GameSettings import GameSettings


class QuadrantMediator(Singleton):

    """
    This class avoids putting UI logic (arcade) in the model class, Quadrant.
    """
    # noinspection SpellCheckingInspection
    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        self._gameEngine:   GameEngine   = GameEngine()
        self._gameState:    GameState    = GameState()
        self._gameSettings: GameSettings = GameSettings()
        self._computer:     Computer     = Computer()

        self._ktm: KlingonTorpedoMediator        = KlingonTorpedoMediator()
        self._ctm: CommanderTorpedoMediator      = CommanderTorpedoMediator()
        self._ptm: EnterpriseTorpedoMediator     = EnterpriseTorpedoMediator()
        self._stm: SuperCommanderTorpedoMediator = SuperCommanderTorpedoMediator()

        self._em:  EnterpriseMediator            = EnterpriseMediator()
        self._km:  KlingonMediator               = KlingonMediator()
        self._cm:  CommanderMediator             = CommanderMediator()
        self._scm: SuperCommanderMediator        = SuperCommanderMediator()

        self._epm: EnterprisePhaserMediator      = EnterprisePhaserMediator()

        self._messageConsole: MessageConsole = MessageConsole()

        self._playerList:         SpriteList = SpriteList()
        self._klingonList:        SpriteList = SpriteList()
        self._commanderList:      SpriteList = SpriteList()
        self._superCommanderList: SpriteList = SpriteList()

        self._soundUnableToComply: Sound = cast(Sound, None)
        self._soundDocked:         Sound = cast(Sound, None)

        self._loadSounds()

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
        self._klingonList     = newValues

    @property
    def commanderList(self) -> SpriteList:
        return self._commanderList

    @commanderList.setter
    def commanderList(self, newValues: SpriteList):
        self._commanderList = newValues

    @property
    def superCommanderList(self) -> SpriteList:
        return self._superCommanderList

    @superCommanderList.setter
    def superCommanderList(self, newValues: SpriteList):
        self._superCommanderList = newValues

    def fireEnterpriseTorpedoes(self, quadrant: Quadrant):
        self._ptm.fireEnterpriseTorpedoesAtKlingons(quadrant=quadrant)

    def firePhasers(self, quadrant: Quadrant):
        self._epm.firePhasers(quadrant=quadrant)

    def dock(self, quadrant: Quadrant):
        """
        TODO:  Move this code to a more relevant place
        Args:
            quadrant:
        """

        if quadrant.hasStarBase is False:
            self._soundUnableToComply.play(volume=self._gameSettings.soundVolume.value)
            self._messageConsole.displayMessage(f'No Star Base in quadrant')
            return
        shipPosition: Coordinates = quadrant.enterprise.gameCoordinates
        basePosition: Coordinates = quadrant.starBase.gameCoordinates
        if self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition) is True:
            self._gameState.shipCondition = ShipCondition.Docked
            self._gameEngine.resetEnergyLevels()
            self._messageConsole.displayMessage(f'Docked.')
            self._soundDocked.play(volume=self._gameSettings.soundVolume.value)
        else:
            self._soundUnableToComply.play(volume=self._gameSettings.soundVolume.value)
            self._messageConsole.displayMessage(f'You are not adjacent to base')

    # noinspection PyUnusedLocal
    def handleMousePress(self, quadrant: Quadrant, arcadePoint: ArcadePoint, button: int, keyModifiers: int):

        if button == MOUSE_BUTTON_RIGHT:
            self._em.impulse(quadrant=quadrant, arcadePoint=arcadePoint)

    def draw(self, quadrant: Quadrant):
        self.playerList.draw()
        self.klingonList.draw()
        self.commanderList.draw()
        self.superCommanderList.draw()
        self._ktm.draw()
        self._ctm.draw()
        self._stm.draw()
        self._ptm.draw(quadrant=quadrant)
        self._epm.draw(quadrant=quadrant)
        if quadrant.hasPlanet is True:
            quadrant.planet.draw()
        if quadrant.hasStarBase is True:
            quadrant.starBase.draw()

    def update(self, quadrant: Quadrant):

        if self.logger.getEffectiveLevel() == DEBUG:
            self.logger.debug(f'{quadrant.enterpriseCoordinates=}')
            if quadrant.klingonCount > 0:
                self.logger.debug(f'{quadrant.klingonCount=}')

        self._updateQuadrant(quadrant)
        self.playerList.update()

        self._ktm.update(quadrant=quadrant)
        self._ctm.update(quadrant=quadrant)
        self._ptm.update(quadrant=quadrant)
        self._stm.update(quadrant=quadrant)
        self._epm.update(quadrant=quadrant)

    def _updateQuadrant(self, quadrant):
        for y in range(QUADRANT_ROWS):
            for x in range(QUADRANT_COLUMNS):

                sector: Sector = quadrant.getSector(Coordinates(x, y))
                self.logger.debug(f'{sector}')

                gamePiece: GamePiece = sector.sprite
                sectorType: SectorType = sector.type

                if sectorType != SectorType.EMPTY:
                    if sectorType == SectorType.ENTERPRISE:
                        self._em.update(quadrant=quadrant)
                    elif sectorType == SectorType.KLINGON:
                        self._km.update(quadrant=quadrant, klingon=cast(Klingon, gamePiece))
                    elif self._noUpdateSector(sectorType=sectorType) is True:
                        pass
                    elif sectorType == SectorType.COMMANDER:
                        self._cm.update(quadrant=quadrant, commander=cast(Commander, gamePiece))
                    elif sectorType == sectorType.SUPER_COMMANDER:
                        self._scm.update(quadrant=quadrant, superCommander=cast(SuperCommander, gamePiece))
                    else:
                        assert False, 'Bad Game Piece'

    def _noUpdateSector(self, sectorType: SectorType) -> bool:
        """
        Some sector have sprites that do not move or are transient and handled by the mediators;
        Args:
            sectorType:

        Returns:   True for the mediator handled sectors or for static sprites
        """
        ans: bool = False

        if sectorType == SectorType.PLANET or sectorType == SectorType.KLINGON_TORPEDO_MISS or \
                sectorType == SectorType.ENTERPRISE_TORPEDO_MISS or sectorType == SectorType.STARBASE:
            ans = True

        return ans

    def _loadSounds(self):

        self._soundUnableToComply = BaseMediator.loadSound(bareFileName='unableToComply.wav')
        self._soundDocked         = BaseMediator.loadSound(bareFileName='Docked.wav')
