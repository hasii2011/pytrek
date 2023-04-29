
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.GameState import GameState

from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.futures.EventEngine import EventEngine
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.mediators.GalaxyMediator import GalaxyMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings

from tests.TestBase import TestBase

from pytrek.engine.futures.FutureEventHandlers import FutureEventHandlers
from pytrek.gui.LogMessageConsole import LogMessageConsole


class TestFutureEventHandlers(TestBase):
    """
    """
    MAX_LOOPS = 128

    clsGameSettings: GameSettings = cast(GameSettings, None)
    clsGameState:    GameState    = cast(GameState, None)
    clsGameEngine:   GameEngine   = cast(GameEngine, None)
    clsIntelligence: Intelligence = cast(Intelligence, None)
    clsComputer:     Computer     = cast(Computer, None)
    clsGalaxy:       Galaxy       = cast(Galaxy, None)

    clsEventEngine:      EventEngine      = cast(EventEngine, None)
    clsQuadrantMediator: QuadrantMediator = cast(QuadrantMediator, None)
    clsGalaxyMediator:   GalaxyMediator   = cast(GalaxyMediator, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpClass()

        TestFutureEventHandlers._setupGame()
        TestFutureEventHandlers.clsLogger.debug(f'Running TestFutureEventHandlers')

    def setUp(self):
        super().setUp()

        self._gameSettings: GameSettings = TestFutureEventHandlers.clsGameSettings
        self._gameState:    GameState    = TestFutureEventHandlers.clsGameState
        self._gameEngine:   GameEngine   = TestFutureEventHandlers.clsGameEngine
        self._intelligence: Intelligence = TestFutureEventHandlers.clsIntelligence
        self._computer:     Computer     = TestFutureEventHandlers.clsComputer
        self._galaxy:       Galaxy       = TestFutureEventHandlers.clsGalaxy

        self._eventEngine:      EventEngine        = TestFutureEventHandlers.clsEventEngine
        self._quadrantMediator: QuadrantMediator   = TestFutureEventHandlers.clsQuadrantMediator
        self._galaxyMediator:   GalaxyMediator     = TestFutureEventHandlers.clsGalaxyMediator
        self._eventHandlers:    FutureEventHandlers = FutureEventHandlers(LogMessageConsole())

    def testSuperNovaEventHandlerKlingonsAreDead(self):

        self._setupGame()
        fEvent: FutureEvent = self._generateArtificialEvent(FutureEventType.SUPER_NOVA)
        self._testEnemyDeadHandler(fEvent=fEvent, enemyName='Klingon')

    def testSuperNovaEventHandlerCommandersAreDead(self):

        self._setupGame()
        fEvent: FutureEvent = self._generateArtificialEvent(FutureEventType.SUPER_NOVA)
        self._testEnemyDeadHandler(fEvent=fEvent, enemyName='Commander')

    def testSuperNovaEventHandlerSuperCommandersAreDead(self):

        self._setupGame()
        fEvent: FutureEvent = self._generateArtificialEvent(FutureEventType.SUPER_NOVA)
        self._testEnemyDeadHandler(fEvent=fEvent, enemyName='SuperCommander')

    def testSuperNovaEventStarBaseDestroyed(self):

        self._setupGame()
        fEvent:                FutureEvent = self._generateArtificialEvent(FutureEventType.SUPER_NOVA)
        previousStarBaseCount: int         = self._gameState.starBaseCount

        self._eventHandlers.superNovaEventHandler(futureEvent=fEvent)

        if previousStarBaseCount != 0:
            expectedStarBaseCount: int = previousStarBaseCount - 1
        else:
            expectedStarBaseCount = 0

        actualStarBaseCount: int = self._gameState.starBaseCount

        self.assertEqual(expectedStarBaseCount, actualStarBaseCount, 'StarBase not properly destroyed')

    def testSuperNovaEventPlanetDestroyed(self):

        self._setupGame()

        fEvent:              FutureEvent = self._generateArtificialEvent(FutureEventType.SUPER_NOVA)
        previousPlanetCount: int         = self._gameState.planetCount

        self._eventHandlers.superNovaEventHandler(futureEvent=fEvent)

        if previousPlanetCount != 0:
            expectedPlanetCount: int = previousPlanetCount - 1
        else:
            expectedPlanetCount = 0

        actualPlanetCount: int = self._gameState.planetCount

        self.assertEqual(expectedPlanetCount, actualPlanetCount, 'Planet not properly destroyed')

    def testSuperNovaEventStarBaseDestroyedNeverNegative(self):
        """
        Destroy all the StarBases and then try one more time
        """
        self._setupGame()
        self.logger.debug(f'Before starbase count: {self._gameState.starBaseCount}')
        quadrant:    Quadrant    = self._getATestEventQuadrant()
        coordinates: Coordinates = quadrant.coordinates
        self.logger.debug(f'After starbase count: {self._gameState.starBaseCount}')

        fEvent:   FutureEvent = FutureEvent()

        fEvent.type                = FutureEventType.SUPER_NOVA
        fEvent.starDate            = self._gameState.starDate
        fEvent.quadrantCoordinates = coordinates

        gameState: GameState = self._gameState
        maxSearches: int     = 0
        while self._gameState.starBaseCount > 0:
            if maxSearches > TestFutureEventHandlers.MAX_LOOPS:
                break
            if coordinates is None:
                self.logger.warning(f'Random starbase search failed try again')
                coordinates = self._galaxy.getStarBaseCoordinates()
                maxSearches += 1
                continue
            else:
                fEvent.quadrantCoordinates = coordinates
                self._eventHandlers.superNovaEventHandler(futureEvent=fEvent)

                counts: str = (
                    f'{coordinates=} '
                    f'remainingKlingons={gameState.remainingKlingons} '
                    f'remainingCommanders={gameState.remainingCommanders} '
                    f'remainingSuperCommanders={gameState.remainingSuperCommanders} '
                    f'starBaseCount={gameState.starBaseCount}'
                )
                self.logger.info(counts)
                coordinates = self._galaxy.getStarBaseCoordinates()
                maxSearches += 1

        if maxSearches < TestFutureEventHandlers.MAX_LOOPS:
            self.assertEqual(0, self._gameState.starBaseCount, 'Did not destroy all StarBases')

            coordinates                = self._intelligence.generateQuadrantCoordinates()
            fEvent.type                = FutureEventType.SUPER_NOVA
            fEvent.starDate            = self._gameState.starDate
            fEvent.quadrantCoordinates = coordinates

            self._eventHandlers.superNovaEventHandler(futureEvent=fEvent)
            self.assertEqual(0, self._gameState.starBaseCount, 'Should be zero all StarBases destroyed')
        else:
            self.logger.warning(f'Too many starbase searches;  testSuperNovaEventStarBaseDestroyedNeverNegative did not run')

    def testTractorBeamEventHandler(self):
        """
        """
        self.logger.debug(f'{self._gameState=}')

        # Simulate game start up
        enterprise: Enterprise = self._gameState.enterprise

        self._quadrant: Quadrant = self._galaxy.currentQuadrant

        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates

        self._quadrantMediator.enterQuadrant(quadrant=self._quadrant, enterprise=enterprise)

        eventHandlers: FutureEventHandlers = FutureEventHandlers(LogMessageConsole())

        coordinates: Coordinates = self._galaxy.currentQuadrant.coordinates

        fEvent:   FutureEvent = FutureEvent()

        fEvent.type                = FutureEventType.SUPER_NOVA
        fEvent.starDate            = self._gameState.starDate
        fEvent.quadrantCoordinates = coordinates

        previousOpTime: float = self._gameState.opTime
        eventHandlers.tractorBeamEventHandler(futureEvent=fEvent)

        self.logger.debug(f'testTractorBeamEventHandler - {self._gameState=}')
        currentOptTime: float = self._gameState.opTime
        self.assertNotEqual(previousOpTime, currentOptTime, 'Operation time did not change')

    def testCommanderAttacksBaseEventHandler(self):
        """
        """
        self._setupGame()

        self._eventEngine.makeUnSchedulable(FutureEventType.TRACTOR_BEAM)

        fEvent: FutureEvent = self._generateArtificialEvent(FutureEventType.COMMANDER_ATTACKS_BASE)

        self._eventHandlers.commanderAttacksBaseEventHandler(futureEvent=fEvent)

    def _generateArtificialEvent(self, eventType: FutureEventType) -> FutureEvent:

        fEvent: FutureEvent = FutureEvent()
        fEvent.type = eventType
        fEvent.starDate = self._gameState.starDate

        quadrant: Quadrant = self._getATestEventQuadrant()
        fEvent.quadrantCoordinates = quadrant.coordinates

        return fEvent

    def _getATestEventQuadrant(self) -> Quadrant:
        """
        Ensure the game is in a legal state for
        Returns:
        """

        coordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
        quadrant:    Quadrant    = self._galaxy.getQuadrant(quadrantCoordinates=coordinates)

        self.logger.debug(f'{quadrant.hasSuperNova=}')
        quadrant.addKlingon()
        quadrant.addCommander()
        quadrant.addSuperCommander()

        if quadrant.hasPlanet is False:
            self._gameState.planetCount += 1
            quadrant.addPlanet()
        if quadrant.hasStarBase is False:
            self._gameState.starBaseCount += 1
            quadrant.addStarBase()
        #
        # Update the game state to reflect what I did here
        #
        self._gameState.remainingKlingons        += 1
        self._gameState.remainingCommanders      += 1
        self._gameState.remainingSuperCommanders += 1

        return quadrant

    def _testEnemyDeadHandler(self, fEvent: FutureEvent, enemyName: str):
        """
        Runs the appropriate count test

        Args:
            fEvent:     Artificial event
            enemyName:  The enemy name, 'Klingon', 'Commander', 'SuperCommander'

        I normally don't like to write dynamically generated codes like this.  However,
        I could not in good conscience duplicate this code three times;  I know it is
        very 'Pythonic', but very high maintenance
        """
        quadrant: Quadrant = self._galaxy.getQuadrant(fEvent.quadrantCoordinates)
        gsPropertyName: str = f'remaining{enemyName}s'
        qPropertyName:  str = f'{enemyName[0].lower()}{enemyName[1:]}Count'

        beforeEnemyCount:   int = getattr(self._gameState, gsPropertyName)
        quadrantEnemyCount: int = getattr(quadrant, qPropertyName)

        self._eventHandlers.superNovaEventHandler(futureEvent=fEvent)
        actualEnemyCount: int = getattr(quadrant, qPropertyName)
        self.assertEqual(0, actualEnemyCount, f'Not all {enemyName}s are dead')

        expectedRemainingEnemies: int = beforeEnemyCount - quadrantEnemyCount
        actualRemainingEnemies:   int = getattr(self._gameState, gsPropertyName)

        self.assertEqual(expectedRemainingEnemies, actualRemainingEnemies, f'Game State was not updated for {enemyName}s')

    @classmethod
    def _setupGame(cls):
        """
        Assumes the game setting location has been set

        Since the game mechanics are run by singletons set them up once
        at the start of this test class.  Then each instance test will just
        use the pre-initialized singletons

        The initialization code copied from PyTrekView
        TODO: perhaps should go in a utility class so it is always current

        """
        TestBase.resetSingletons()

        TestFutureEventHandlers.clsGameSettings = GameSettings()     # Be able to read the preferences file
        TestFutureEventHandlers.clsGameState    = GameState()        # Set up the game parameters which uses the above
        TestFutureEventHandlers.clsGameEngine   = GameEngine()       # Then the engine needs to be initialized
        TestFutureEventHandlers.clsIntelligence = Intelligence()
        TestFutureEventHandlers.clsComputer     = Computer()
        TestFutureEventHandlers.clsGalaxy       = Galaxy()
        TestFutureEventHandlers.clsEventEngine  = EventEngine(LogMessageConsole())
        TestFutureEventHandlers.clsQuadrantMediator = QuadrantMediator()
        TestFutureEventHandlers.clsGalaxyMediator   = GalaxyMediator()      # This essentially finishes initializing most of the game


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestFutureEventHandlers))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
