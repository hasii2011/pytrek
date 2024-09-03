
from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.GameType import GameType
from pytrek.engine.PlayerType import PlayerType
from pytrek.model.Coordinates import Coordinates
from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.SoundVolume import SoundVolume
from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds

from tests.ProjectTestBase import ProjectTestBase


class TestGameSettings(ProjectTestBase):
    """
    """
    def setUp(self):
        super().setUp()
        self._settings: GameSettings = GameSettings()

    def testMaxStarsExistence(self):
        self.assertIsNotNone(self._settings.maximumStars)

    def testMaxStarBasesExistence(self):
        self.assertIsNotNone(self._settings.maximumStarBases)

    def testMinStarBasesExistence(self):
        self.assertIsNotNone(self._settings.minimumStarBases)

    def testMaxPlanetsExistence(self):
        self.assertIsNotNone(self._settings.maximumPlanets)

    def testInitialEnergyLevelExistence(self):
        self.assertIsNotNone(self._settings.initialEnergyLevel)

    def testInitialShieldEnergyExistence(self):
        self.assertIsNotNone(self._settings.initialShieldEnergy)

    def testInitialTorpedoCountExistence(self):
        self.assertIsNotNone(self._settings.initialTorpedoCount)

    def testMinimumImpulseEnergyExistence(self):
        self.assertIsNotNone(self._settings.minimumImpulseEnergy)

    def testDefaultWarpFactorExistence(self):
        self.assertIsNotNone(self._settings.defaultWarpFactor)

    def testPhaserFactor(self):
        self.assertEqual(2.0, self._settings.phaserFactor, 'Looks like we change the default phaser power factor')

    def testPlayerTypeExistence(self):
        self.assertIsNotNone(self._settings.playerType)

    def testGameTypeExistence(self):
        self.assertIsNotNone(self._settings.gameType)

    def testGameLengthFactorExistence(self):
        self.assertIsNotNone(self._settings.gameLengthFactor)

    def testStarBaseExtenderExistence(self):
        self.assertIsNotNone(self._settings.starBaseExtender)

    def testStarBaseMultiplierExistence(self):
        self.assertIsNotNone(self._settings.starBaseMultiplier)

    def testMinKlingonFiringIntervalExistence(self):
        self.assertIsNotNone(self._settings.minKlingonFiringInterval)

    def testMaxKlingonFiringIntervalExistence(self):
        self.assertIsNotNone(self._settings.maxKlingonFiringInterval)

    def testMinCommanderFiringIntervalExistence(self):
        self.assertIsNotNone(self._settings.minCommanderFiringInterval)

    def testMaxCommanderFiringIntervalExistence(self):
        self.assertIsNotNone(self._settings.maxCommanderFiringInterval)

    def testPhaserBurstToTerminateExistence(self):
        self.assertIsNotNone(self._settings.phaserBurstToTerminate)

    def testNoviceTorpedoSpeeds(self):

        tpNovice: TorpedoSpeeds = self._settings.noviceTorpedoSpeeds

        self.assertIsNotNone(tpNovice, 'We should at least get an object back')

        self.assertEqual(1, tpNovice.superCommander)

    def testFairTorpedoSpeeds(self):

        tpFair: TorpedoSpeeds = self._settings.fairTorpedoSpeeds

        self.assertIsNotNone(tpFair, 'We should at least get an object back')

        self.assertEqual(1, tpFair.superCommander)

    def testGoodTorpedoSpeeds(self):

        tpGood: TorpedoSpeeds = self._settings.goodTorpedoSpeeds

        self.assertIsNotNone(tpGood, 'We should at least get an object back')

        self.assertEqual(4, tpGood.superCommander)

    def testExpertTorpedoSpeeds(self):

        tpExpert: TorpedoSpeeds = self._settings.expertTorpedoSpeeds

        self.assertIsNotNone(tpExpert, 'We should at least get an object back')

        self.assertEqual(4, tpExpert.commander)
        self.assertEqual(4, tpExpert.superCommander)

    def testEmeritusTorpedoSpeeds(self):

        tpEmeritus: TorpedoSpeeds = self._settings.emeritusTorpedoSpeeds

        self.assertIsNotNone(tpEmeritus, 'We should at least get an object back')

        self.assertEqual(5, tpEmeritus.commander)
        self.assertEqual(5, tpEmeritus.superCommander)

    def testDebugSettingsAddKlingons(self):

        saveSetting: bool = self._settings.addKlingons
        self._settings.addKlingons = True
        self.assertTrue(self._settings.addKlingons, 'Supposed to change')
        self._settings.addKlingons = saveSetting

    def testDebugSettingsDebugKlingonCount(self):

        saveSetting: int = self._settings.klingonCount
        self._settings.klingonCount = 22
        self.assertEqual(22, self._settings.klingonCount, 'Supposed to change')
        self._settings.klingonCount = saveSetting

    def testDebugPrintKlingonPlacement(self):

        saveSetting: bool = self._settings.printKlingonPlacement
        self._settings.printKlingonPlacement = True
        self.assertTrue(self._settings.printKlingonPlacement, 'Should have changed to non-default')
        self._settings.printKlingonPlacement = saveSetting

    def testMaxStarbaseSearches(self):
        saveSetting: int = self._settings.maxStarbaseSearches
        self._settings.maxStarbaseSearches = 42
        self.assertEqual(42, self._settings.maxStarbaseSearches, 'Value did not change')
        self._settings.maxStarbaseSearches = saveSetting

    def testMaxCommanderSearches(self):
        saveSetting: int = self._settings.maxCommanderSearches
        self._settings.maxStarbaseSearches = 69
        self.assertEqual(69, self._settings.maxStarbaseSearches, 'Value did not change')
        self._settings.maxStarbaseSearches = saveSetting

    def testSuperNovaSchedulable(self):
        saveSetting: bool = self._settings.scheduleSuperNova
        self._settings.scheduleSuperNova = False
        self.assertEqual(False, self._settings.scheduleSuperNova, 'Value did not change')
        self._settings.scheduleSuperNova = saveSetting

    def testTractorBeamSchedulable(self):
        saveSetting: bool = self._settings.scheduleTractorBeam
        self._settings.scheduleTractorBeam = False
        self.assertEqual(False, self._settings.scheduleTractorBeam, 'Value did not change')
        self._settings.scheduleTractorBeam = saveSetting

    def testsCommanderAttacksBaseSchedulable(self):
        saveSetting: bool = self._settings.scheduleCommanderAttacksBase
        self._settings.scheduleCommanderAttacksBase = False
        self.assertEqual(False, self._settings.scheduleCommanderAttacksBase, 'Value did not change')
        self._settings.scheduleCommanderAttacksBase = saveSetting

    def testDebugManualPlaceShipInQuadrant(self):

        saveSetting: bool = self._settings.manualPlaceShipInQuadrant
        if saveSetting is False:
            self._settings.manualPlaceShipInQuadrant = True
            actualValue: bool = self._settings.manualPlaceShipInQuadrant
            self.assertEqual(True, actualValue, 'Value did not change to True')
        else:
            self._settings.manualPlaceShipInQuadrant = False
            actualValue = self._settings.manualPlaceShipInQuadrant
            self.assertEqual(False, actualValue, 'Value did not change to False')

        self._settings.manualPlaceShipInQuadrant = saveSetting

    def testManualSectorCoordinates(self):
        saveSetting: Coordinates = self._settings.manualSectorCoordinates

        expectedCoordinates: Coordinates = Coordinates(x=7, y=7)
        self._settings.manualSectorCoordinates = expectedCoordinates
        actualCoordinates: Coordinates = self._settings.manualSectorCoordinates

        self.assertEqual(expectedCoordinates, actualCoordinates, 'Ship manual positioning coordinates did not change')

        self._settings.manualSectorCoordinates = saveSetting

    def testPower(self):

        gameSettings: GameSettings = GameSettings()

        self.assertEqual(5000, gameSettings.initialEnergyLevel,              'Initial Energy default must have changed')
        self.assertEqual(2.0,  gameSettings.phaserFactor,                    'Should be a float')

    def testFactors(self):
        gameSettings: GameSettings = GameSettings()
        self.assertEqual(2.0,  gameSettings.starBaseExtender,                'Bad star base extender')
        self.assertEqual(15,   gameSettings.maxKlingonFiringInterval,        'Bad interval')
        self.assertEqual(10,   gameSettings.maxCommanderFiringInterval,      'Bad max commander firing interval')
        self.assertEqual(8,    gameSettings.maxSuperCommanderFiringInterval, 'Bad max commander firing interval')
        self.assertEqual(5,    gameSettings.minKlingonMoveInterval,          'Bad min Klingon move interval')
        self.assertEqual(3,    gameSettings.minCommanderMoveInterval,        'Bad min Commander move interval')
        self.assertEqual(0.2,  gameSettings.photonTorpedoMisfireRate,        'Bad misfire rate')

    def testGetDeveloper(self):
        gameSettings: GameSettings = GameSettings()

        self.assertEqual(128,  gameSettings.maxStarbaseSearches)
        self.assertEqual(128,   gameSettings.maxCommanderSearches)

    def testSetDeveloper(self):
        gameSettings: GameSettings = GameSettings()

        gameSettings.maxStarbaseSearches = 500
        self.assertEqual(500,  gameSettings.maxStarbaseSearches)
        gameSettings.maxStarbaseSearches = 128

    def testGetDebug(self):

        gameSettings: GameSettings = GameSettings()

        self.assertFalse(gameSettings.manualPlaceShipInQuadrant,                  'Manual ship placement should be off')
        self.assertEqual(Coordinates(0, 0), gameSettings.manualSectorCoordinates, 'These are wrong')

        self.assertFalse(gameSettings.addCommanders,         'addCommanders should be off')
        self.assertFalse(gameSettings.addKlingons,           'addKlingons should be off')
        self.assertFalse(gameSettings.addPlanet,             'No extra planets')
        self.assertFalse(gameSettings.debugBaseEnemyTorpedo, 'We do not want debug on for enemy torpedoes')

    def testSetDebug(self):
        gameSettings: GameSettings = GameSettings()
        gameSettings.manualSectorCoordinates = Coordinates(3, 3)
        self.assertEqual(Coordinates(3, 3), gameSettings.manualSectorCoordinates, 'Debug Setting Manual Coordinates is wrong')
        gameSettings.manualSectorCoordinates = Coordinates(0, 0)

    def testSetDebug2(self):
        gameSettings: GameSettings = GameSettings()
        gameSettings.commanderCount = 99
        self.assertEqual(99, gameSettings.commanderCount, 'Commander count is not correct')
        gameSettings.commanderCount = 1

    def testSetDebug5(self):
        gameSettings: GameSettings = GameSettings()
        gameSettings.debugBaseEnemyTorpedoInterval = 6666
        self.assertEqual(6666, gameSettings.debugBaseEnemyTorpedoInterval, 'Temporarily evil')
        gameSettings.debugBaseEnemyTorpedoInterval = 20

    def testSetDebug3(self):
        gameSettings: GameSettings = GameSettings()
        gameSettings.addPlanet = True
        self.assertTrue(gameSettings.addPlanet, 'Temporarily True')
        gameSettings.addPlanet = False

    def testSetDebug4(self):
        gameSettings: GameSettings = GameSettings()
        gameSettings.debugBaseEnemyTorpedo = True
        self.assertTrue(gameSettings.debugBaseEnemyTorpedo, 'Temporarily True')
        gameSettings.debugBaseEnemyTorpedo = False

    def testGetNoviceTorpedoSpeed(self):
        gameSettings: GameSettings = GameSettings()

        expectedTS: TorpedoSpeeds = TorpedoSpeeds.toTorpedoSpeed('5,2,2,1')
        actualTS:   TorpedoSpeeds = gameSettings.noviceTorpedoSpeeds

        self.assertEqual(expectedTS, actualTS, 'Torpedo speeds do not match')

    def testGetEmeritusTorpedoSpeed(self):
        gameSettings: GameSettings = GameSettings()

        expectedTS: TorpedoSpeeds = TorpedoSpeeds.toTorpedoSpeed('1,2,5,5')
        actualTS:   TorpedoSpeeds = gameSettings.emeritusTorpedoSpeeds

        self.assertEqual(expectedTS, actualTS, 'Torpedo speeds do not match')

    def testGetGameLevelSettings1(self):

        gameSettings: GameSettings = GameSettings()

        playerType: PlayerType = gameSettings.playerType
        self.assertIsInstance(playerType, PlayerType, 'Enum getter does not work')

    def testGetGameLevelSettings2(self):

        gameSettings: GameSettings = GameSettings()

        gameType: GameType = gameSettings.gameType
        self.assertIsInstance(gameType, GameType, 'Enum getter does not work')

    def testGetGameLevelSettings3(self):

        gameSettings: GameSettings = GameSettings()

        soundVolume: SoundVolume = gameSettings.soundVolume
        self.assertIsInstance(soundVolume, SoundVolume, 'Enum getter does not work')

    def testSetGameLevelSettings(self):

        gameSettings: GameSettings = GameSettings()

        saveGameType: GameType = gameSettings.gameType

        gameSettings.gameType = GameType.Long

        self.assertEqual(GameType.Long, gameSettings.gameType, 'Setter did not work')

        gameSettings.gameType = saveGameType

    def testGetDamageAdjuster(self):
        gameSettings: GameSettings = GameSettings()

        damageAdjusterValue: float = gameSettings.damageAdjuster

        self.assertTrue(0.0 < damageAdjusterValue, 'Should be a positive value')

    def testSetDamageAdjuster(self):

        gameSettings: GameSettings = GameSettings()

        expectedValue: float = 0.75
        saveValue:     float = gameSettings.damageAdjuster  # Save it

        gameSettings.damageAdjuster = expectedValue

        setValue: float = gameSettings.damageAdjuster

        gameSettings.damageAdjuster = saveValue         # Restore it before we assert it

        self.assertEqual(0.75, setValue, 'Not correctly set')

    def testGetSetDebugEvents(self):
        gameSettings: GameSettings = GameSettings()

        saveDebugEvents: bool = gameSettings.debugEvents

        gameSettings.debugEvents = False

        self.assertFalse(gameSettings.debugEvents, 'Should be off')

        gameSettings.debugEvents = saveDebugEvents


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGameSettings))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
