
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG

from arcade import SpriteList

from hasiihelper.Singleton import Singleton

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS

from pytrek.GameState import GameState
from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType

from pytrek.engine.Computer import Computer
from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.ShipCondition import ShipCondition
from pytrek.gui.MessageConsole import MessageConsole
from pytrek.gui.gamepieces.base.BaseGamePiece import BaseGamePiece

from pytrek.gui.gamepieces.commander.Commander import Commander

from pytrek.gui.gamepieces.klingon.Klingon import Klingon
from pytrek.gui.gamepieces.supercommander.SuperCommander import SuperCommander

from pytrek.mediators.CommanderMediator import CommanderMediator
from pytrek.mediators.CommanderTorpedoMediator import CommanderTorpedoMediator
from pytrek.mediators.EnterprisePhaserMediator import EnterprisePhaserMediator
from pytrek.mediators.KlingonMediator import KlingonMediator
from pytrek.mediators.KlingonTorpedoMediator import KlingonTorpedoMediator
from pytrek.mediators.EnterpriseTorpedoMediator import EnterpriseTorpedoMediator
from pytrek.mediators.SuperCommanderMediator import SuperCommanderMediator
from pytrek.mediators.SuperCommanderTorpedoMediator import SuperCommanderTorpedoMediator

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.settings.GameSettings import GameSettings


class QuadrantMediator(Singleton):
    """
    This class avoids implementing UI logic (arcade) in the model class, Quadrant.
    """
    # noinspection PyAttributeOutsideInit
    def init(self, *args, **kwargs):

        self.logger: Logger = getLogger(__name__)

        self._gameEngine:   GameEngine   = GameEngine()
        self._gameState:    GameState    = GameState()
        self._gameSettings: GameSettings = GameSettings()
        self._computer:     Computer     = Computer()
        self._intelligence: Intelligence = Intelligence()

        self._ktm: KlingonTorpedoMediator        = KlingonTorpedoMediator()
        self._ctm: CommanderTorpedoMediator      = CommanderTorpedoMediator()
        self._ptm: EnterpriseTorpedoMediator     = EnterpriseTorpedoMediator()
        self._stm: SuperCommanderTorpedoMediator = SuperCommanderTorpedoMediator()

        self._km:  KlingonMediator               = KlingonMediator()
        self._cm:  CommanderMediator             = CommanderMediator()
        self._scm: SuperCommanderMediator        = SuperCommanderMediator()

        self._epm: EnterprisePhaserMediator      = EnterprisePhaserMediator()

        self._messageConsole: MessageConsole = MessageConsole()
        self._soundMachine:   SoundMachine   = SoundMachine()

        self._playerList:         SpriteList = SpriteList()
        self._klingonList:        SpriteList = SpriteList()
        self._commanderList:      SpriteList = SpriteList()
        self._superCommanderList: SpriteList = SpriteList()

    @property
    def playerList(self) -> SpriteList:
        return self._playerList

    # noinspection PyAttributeOutsideInit
    @playerList.setter
    def playerList(self, newValues: SpriteList):
        self._playerList = newValues

    @property
    def klingonList(self) -> SpriteList:
        return self._klingonList

    # noinspection PyAttributeOutsideInit
    @klingonList.setter
    def klingonList(self, newValues: SpriteList):
        self._klingonList     = newValues

    @property
    def commanderList(self) -> SpriteList:
        return self._commanderList

    # noinspection PyAttributeOutsideInit
    @commanderList.setter
    def commanderList(self, newValues: SpriteList):
        self._commanderList = newValues

    @property
    def superCommanderList(self) -> SpriteList:
        return self._superCommanderList

    # noinspection PyAttributeOutsideInit
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
            self._soundMachine.playSound(soundType=SoundType.UnableToComply)
            self._messageConsole.displayMessage(f'No Star Base in quadrant')
            return
        shipPosition: Coordinates = quadrant.enterprise.gameCoordinates
        basePosition: Coordinates = quadrant.starBase.gameCoordinates
        if self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition) is True:
            self._gameState.shipCondition = ShipCondition.Docked
            self._gameEngine.resetEnergyLevels()
            self._messageConsole.displayMessage(f'Docked.')
            self._soundMachine.playSound(SoundType.Docked)
        else:
            self._soundMachine.playSound(SoundType.UnableToComply)
            self._messageConsole.displayMessage(f'You are not adjacent to base')

    def enterQuadrant(self, quadrant: Quadrant, enterprise):

        currentSectorCoordinates: Coordinates = self._intelligence.generateSectorCoordinates()

        if self._gameSettings.debugManualPlaceShipInQuadrant is True:
            currentSectorCoordinates = self._gameSettings.manualSectorCoordinates

        playerList: SpriteList = SpriteList()
        playerList.append(enterprise)

        self._gameState.currentSectorCoordinates = currentSectorCoordinates
        quadrant.placeEnterprise(enterprise, currentSectorCoordinates)

        self.playerList = playerList
        # Don't do this until we have set up the current quadrant
        self._makeEnemySpriteLists(quadrant=quadrant)
        self._doDebugActions(quadrant=quadrant)

    # noinspection PyUnusedLocal
    def handleMousePress(self, quadrant: Quadrant, arcadePoint: ArcadePoint, button: int, keyModifiers: int):
        pass

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

                gamePiece:  BaseGamePiece = sector.sprite
                sectorType: SectorType    = sector.type

                if sectorType != SectorType.EMPTY:
                    if sectorType == SectorType.KLINGON:
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
                sectorType == SectorType.ENTERPRISE_TORPEDO_MISS or sectorType == SectorType.STARBASE or \
                sectorType == SectorType.ENTERPRISE:
            ans = True

        return ans

    def _makeEnemySpriteLists(self, quadrant: Quadrant):
        """
        Place enemies in the appropriate sprite lists
        Depends on the correct quadrant mediator is in place
        """
        self.__makeKlingonSpriteList(quadrant=quadrant)
        self.__makeCommanderSpriteList(quadrant=quadrant)
        self.__makeSuperCommanderSpriteList(quadrant=quadrant)

    def _doDebugActions(self, quadrant: Quadrant):

        self.__doEnemyDebugActions(quadrant=quadrant)

        if self._gameSettings.debugAddPlanet is True:
            quadrant.addPlanet()

        if self._gameSettings.debugAddStarBase is True:
            quadrant.addStarBase()

    def __makeKlingonSpriteList(self, quadrant: Quadrant):
        if quadrant.klingonCount > 0:
            self._gameState.shipCondition = ShipCondition.Red
            klingonSprites: SpriteList = SpriteList()
            for klingon in quadrant.klingons:
                klingonSprites.append(klingon)

            self.klingonList = klingonSprites
        else:
            self.klingonList = SpriteList()

    def __makeCommanderSpriteList(self, quadrant: Quadrant):
        if quadrant.commanderCount > 0:
            self._gameState.shipCondition = ShipCondition.Red
            commanderSprites: SpriteList = SpriteList()
            for commander in quadrant.commanders:
                commanderSprites.append(commander)

            self.commanderList = commanderSprites
        else:
            self.commanderList = SpriteList()

    def __makeSuperCommanderSpriteList(self, quadrant: Quadrant):
        if quadrant.superCommanderCount > 0:
            self._gameState.shipCondition = ShipCondition.Red
            superCommanderSprites: SpriteList = SpriteList()
            for superCommander in quadrant.superCommanders:
                superCommanderSprites.append(superCommander)

            self.superCommanderList = superCommanderSprites
        else:
            self.superCommanderList = SpriteList()

    def __doEnemyDebugActions(self, quadrant: Quadrant):

        if self._gameSettings.debugAddKlingons is True:
            numKlingons: int = self._gameSettings.debugKlingonCount
            for x in range(numKlingons):
                klingon: Klingon = quadrant.addKlingon()
                self.klingonList.append(klingon)

            self._gameState.remainingKlingons += numKlingons

        if self._gameSettings.debugAddCommanders is True:
            nCommanders: int = self._gameSettings.debugCommanderCount
            for x in range(nCommanders):
                commander: Commander = quadrant.addCommander()
                self.commanderList.append(commander)

            self._gameState.remainingCommanders += nCommanders

        if self._gameSettings.debugAddSuperCommanders:
            nSuperCommanders: int = self._gameSettings.debugSuperCommanderCount
            for x in range(nSuperCommanders):
                superCommander: SuperCommander = quadrant.addSuperCommander()
                self.superCommanderList.append(superCommander)

            self._gameState.remainingSuperCommanders += nSuperCommanders
