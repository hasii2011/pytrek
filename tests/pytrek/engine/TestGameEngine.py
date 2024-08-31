
from typing import Dict
from typing import NewType

from math import degrees

from pytrek.engine.Computer import Computer
from pytrek.engine.Direction import Direction
from pytrek.engine.DirectionData import DirectionData
from pytrek.engine.PlayerType import PlayerType
from pytrek.engine.ShieldHitData import ShieldHitData
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.DeviceManager import DeviceManager

from pytrek.model.Coordinates import Coordinates

from pytrek.settings.GameSettings import GameSettings

from pytrek.GameState import GameState

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.ProjectTestBase import ProjectTestBase

TestedDirections = NewType('TestedDirections', Dict[Direction, bool])


class TestGameEngine(ProjectTestBase):
    """
    """
    def setUp(self):
        super().setUp()
        self._gameSettings: GameSettings = GameSettings()
        self._gameEngine:   GameEngine   = GameEngine()
        self._gameState:    GameState    = GameState()
        self._computer:     Computer     = Computer()

        self._devices:      DeviceManager    = DeviceManager()

    def testComputeHitValueOnKlingon(self):

        testKlingonPower: float = 480.0

        enterprisePosition: Coordinates = Coordinates(x=0, y=0)
        klingonPosition:   Coordinates = Coordinates(x=0, y=9)

        for x in range(10):
            kHit: float = self._gameEngine.computeHitValueOnKlingon(enterprisePosition=enterprisePosition,
                                                                    klingonPosition=klingonPosition,
                                                                    klingonPower=testKlingonPower)

            self.logger.info(f'Iteration: {x} - kHit={kHit:.2f}')

            if kHit <= testKlingonPower:
                self.assertLess(kHit, testKlingonPower, 'Single torpedo can almost never kill a Klingon')
            else:
                self.logger.info(f'Iteration: {x} killed a Klingon')

    def testComputeCourseStraightWest(self):

        end:   Coordinates = Coordinates(x=0, y=5)
        start: Coordinates = Coordinates(x=9, y=5)

        course: float = self._gameEngine._computeCourse(start=start, end=end)
        angle:  float = degrees(course)
        self.assertEqual(180, angle, 'Did calculation chang')
        self.logger.info(f'{course=} {angle=}')

    def testComputeCourseDown(self):

        start: Coordinates = Coordinates(x=0, y=0)
        end:   Coordinates = Coordinates(x=0, y=9)

        course:    float = self._gameEngine._computeCourse(start=start, end=end)
        downAngle: float = degrees(course)

        self.assertEqual(90, downAngle, 'Hmm, messed up code')
        self.logger.info(f'{course=} {downAngle=}')

    def testComputeCourseUp(self):

        start: Coordinates = Coordinates(x=0, y=0)
        end:   Coordinates = Coordinates(x=0, y=9)

        backwardCourse: float = self._gameEngine._computeCourse(start=end, end=start)
        backAngle:      float = degrees(backwardCourse)
        self.assertEqual(-90, backAngle, 'Who changed my code')
        self.logger.info(f'{backwardCourse=} {backAngle=}')

    def testComputeCourseDiagonal(self):

        start: Coordinates = Coordinates(x=0, y=0)
        end:   Coordinates = Coordinates(x=9, y=9)

        course: float = self._gameEngine._computeCourse(start=start, end=end)
        angle:  float = degrees(course)
        self.assertEqual(45, angle, 'Busted code')
        self.logger.info(f'{course=} {angle=}')

    def testComputeCourseBackDiagonal(self):

        start: Coordinates = Coordinates(x=0, y=0)
        end:   Coordinates = Coordinates(x=9, y=9)

        backwardCourse: float = self._gameEngine._computeCourse(start=end, end=start)
        backAngle:      float = degrees(backwardCourse)
        self.assertEqual(-135, backAngle, 'Who changed my code')

        self.logger.info(f'{backwardCourse=}, {backAngle=}')

    def testComputeCourseStraightEast(self):

        start: Coordinates = Coordinates(x=0, y=5)
        end:   Coordinates = Coordinates(x=9, y=5)

        course: float = self._gameEngine._computeCourse(start=start, end=end)
        angle:  float = degrees(course)
        self.assertEqual(0, angle, 'Did calculation chang')
        self.logger.info(f'{course=} {angle=}')

    def testUpdateTimeAfterWarpTravelShortWarpSpeedLow(self):

        previousStarDate:       float = self._gameState.starDate
        previousRemainGameTime: float = self._gameState.remainingGameTime

        travelDistance: float = 1.0
        warpFactor:     float = 1.0

        self._gameEngine.updateTimeAfterWarpTravel(travelDistance=travelDistance, warpFactor=warpFactor)

        updatedOpTime:  float = self._gameState.opTime
        expectedOpTime: float = 10.0

        self.assertEqual(expectedOpTime, updatedOpTime, 'Operation Time incorrectly calculated')

        expectedStarDate: float = previousStarDate + updatedOpTime
        actualStarDate:   float = self._gameState.starDate

        self.assertEqual(expectedStarDate, actualStarDate, 'StarDate was inappropriately updated')

        expectedRemainingGameTime: float = previousRemainGameTime - updatedOpTime
        actualRemainingGameTime:   float = self._gameState.remainingGameTime

        self.assertEqual(expectedRemainingGameTime, actualRemainingGameTime, 'Remaining Game Time was inappropriately updated')

    def testUpdateTimeAfterWarpTravelLong(self):

        previousStarDate: float = self._gameState.starDate
        previousRemainGameTime: float = self._gameState.remainingGameTime

        travelDistance: float = 9.0
        warpFactor:     float = 9.0

        self._gameEngine.updateTimeAfterWarpTravel(travelDistance=travelDistance, warpFactor=warpFactor)

        updatedOpTime:  float = self._gameState.opTime
        expectedOpTime: float = 1.11

        self.assertAlmostEqual(expectedOpTime, updatedOpTime, 2, 'Operation Time incorrectly calculated')

        expectedStarDate: float = previousStarDate + updatedOpTime
        actualStarDate:   float = self._gameState.starDate

        self.assertEqual(expectedStarDate, actualStarDate, 'StarDate was inappropriately updated')

        expectedRemainingGameTime: float = previousRemainGameTime - updatedOpTime
        actualRemainingGameTime:   float = self._gameState.remainingGameTime

        self.assertEqual(expectedRemainingGameTime, actualRemainingGameTime, 'Remaining Game Time was inappropriately updated')

    def testShipAdjacentToBaseNorth(self):
        """
        In these tests the base is always at sector coordinates 5,5
        """

        shipPosition: Coordinates = Coordinates(x=4, y=5)
        basePosition: Coordinates = Coordinates(x=5, y=5)

        adjacent: bool = self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition)

        self.assertTrue(adjacent, 'We are directly north')

    def testShipAdjacentToBaseSouth(self):

        shipPosition: Coordinates = Coordinates(x=5, y=5)
        basePosition: Coordinates = Coordinates(x=6, y=5)

        adjacent: bool = self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition)

        self.assertTrue(adjacent, 'We are directly south')

    def testShipAdjacentToBaseEast(self):

        shipPosition: Coordinates = Coordinates(x=6, y=5)
        basePosition: Coordinates = Coordinates(x=5, y=5)

        adjacent: bool = self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition)

        self.assertTrue(adjacent, 'We are directly east')

    def testShipAdjacentToBaseWest(self):

        shipPosition: Coordinates = Coordinates(x=4, y=5)
        basePosition: Coordinates = Coordinates(x=5, y=5)

        adjacent: bool = self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition)

        self.assertTrue(adjacent, 'We are directly west')

    def testShipAdjacentToBaseNorthEast(self):

        shipPosition: Coordinates = Coordinates(x=4, y=6)
        basePosition: Coordinates = Coordinates(x=5, y=5)

        adjacent: bool = self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition)

        self.assertTrue(adjacent, 'We are directly NorthEast')

    def testShipAdjacentToBaseNorthWest(self):

        shipPosition: Coordinates = Coordinates(x=4, y=4)
        basePosition: Coordinates = Coordinates(x=5, y=5)

        adjacent: bool = self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition)

        self.assertTrue(adjacent, 'We are directly NorthWest')

    def testShipAdjacentToBaseSouthEast(self):

        shipPosition: Coordinates = Coordinates(x=6, y=6)
        basePosition: Coordinates = Coordinates(x=5, y=5)

        adjacent: bool = self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition)

        self.assertTrue(adjacent, 'We are directly SouthEast')

    def testShipAdjacentToBaseSouthWest(self):

        shipPosition: Coordinates = Coordinates(x=6, y=4)
        basePosition: Coordinates = Coordinates(x=5, y=5)

        adjacent: bool = self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition)

        self.assertTrue(adjacent, 'We are directly SouthWest')

    def testShipAdjacentToBaseNotAdjacentClose(self):

        shipPosition: Coordinates = Coordinates(x=7, y=7)
        basePosition: Coordinates = Coordinates(x=5, y=5)

        adjacent: bool = self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition)

        self.assertFalse(adjacent, 'We are pretty close but not adjacent')

    def testShipAdjacentToBaseNotAdjacentVeryFar(self):

        shipPosition: Coordinates = Coordinates(x=9, y=9)
        basePosition: Coordinates = Coordinates(x=5, y=5)

        adjacent: bool = self._gameEngine.shipAdjacentToBase(shipPosition=shipPosition, basePosition=basePosition)

        self.assertFalse(adjacent, 'We are very far and not adjacent')

    def testDoPhasersMaxDistance(self):

        shooterCoordinates: Coordinates = Coordinates(0, 0)
        targetCoordinates:  Coordinates = Coordinates(9, 9)

        expectedPhaserHit: float = 218.6
        self._runPhaserTest(shooterCoordinates=shooterCoordinates, targetCoordinates=targetCoordinates, expectedPhaserHit=expectedPhaserHit)

    def testDoPhasersShortDistance(self):
        shooterCoordinates: Coordinates = Coordinates(0, 4)
        targetCoordinates:  Coordinates = Coordinates(4, 4)

        expectedPhaserHit: float = 239.68
        self._runPhaserTest(shooterCoordinates=shooterCoordinates, targetCoordinates=targetCoordinates, expectedPhaserHit=expectedPhaserHit)

    def testHitThem(self):
        shooterCoordinates: Coordinates = Coordinates(0, 0)
        targetCoordinates:  Coordinates = Coordinates(9, 9)
        distance:           float        = self._computer.computeQuadrantDistance(startSector=shooterCoordinates, endSector=targetCoordinates)
        enemyPower:         float        = 500.0

        powerDrain: float = self._gameEngine.hitThem(distance=distance, hit=218.6, enemyPower=enemyPower)

        minPowerDrain: float = 329

        self.assertGreater(powerDrain, minPowerDrain, 'Did not calculate the minimum power drain')

        self.logger.info(f'{powerDrain=}')

    def testComputeShieldHitShieldsFull(self):

        shieldHitData:  ShieldHitData = self._gameEngine.computeShieldHit(torpedoHit=1000,
                                                                          currentShieldPower=self._gameSettings.defaultFullShields)

        self.assertEqual(shieldHitData.shieldAbsorptionValue,   1000, 'Shields should absorb all')
        self.assertEqual(shieldHitData.degradedTorpedoHitValue, 0,    'Nothing should pass through')

    def testComputeShieldHitShieldsHalf(self):

        shieldHitData:  ShieldHitData = self._gameEngine.computeShieldHit(torpedoHit=1000,
                                                                          currentShieldPower=self._gameSettings.defaultFullShields // 2)

        self.assertEqual(shieldHitData.shieldAbsorptionValue,   500, 'Shields should absorb half')
        self.assertEqual(shieldHitData.degradedTorpedoHitValue, 500, 'Half should pass through')

    def testComputeShieldHitShieldsQuarter(self):

        shieldHitData:  ShieldHitData = self._gameEngine.computeShieldHit(torpedoHit=1000,
                                                                          currentShieldPower=self._gameSettings.defaultFullShields // 4)

        self.assertEqual(shieldHitData.shieldAbsorptionValue,   250, 'Shields should absorb 1/4')
        self.assertEqual(shieldHitData.degradedTorpedoHitValue, 750, '3/4 should pass through')

    def testComputeShieldHitShieldsDown(self):

        saveShieldStatus: DeviceStatus = self._devices.getDeviceStatus(DeviceType.Shields)

        self._devices.setDeviceStatus(DeviceType.Shields, DeviceStatus.Down)

        shieldHitData:  ShieldHitData = self._gameEngine.computeShieldHit(torpedoHit=1000,
                                                                          currentShieldPower=self._gameSettings.defaultFullShields)

        self.assertEqual(shieldHitData.shieldAbsorptionValue,   0,   'Shields are down everything passes through')
        self.assertEqual(shieldHitData.degradedTorpedoHitValue, 1000, 'We should get whacked')

        self._devices.setDeviceStatus(DeviceType.Shields, saveShieldStatus)

    def testComputeHit(self):

        for pType in PlayerType:

            computedHit = self._commonComputeHit(playerType=pType)
            self.assertFalse(computedHit == 0.0, "Can't have non-hit")
            self.logger.info(f"computedHit for {pType.__repr__()}: {computedHit}")

    def testComputeEnergyWhenBlockedNominal(self):

        startSector: Coordinates = Coordinates(x=1, y=1)
        endSector:   Coordinates = Coordinates(x=5, y=5)

        expectedStopEnergy: float = 76.57
        decimalPlace:       int   = 2

        stopEnergy: float = self._gameEngine.computeEnergyWhenBlocked(startSector=startSector, endSector=endSector)

        self.logger.info(f'{stopEnergy}')

        self.assertAlmostEqual(expectedStopEnergy, stopEnergy, decimalPlace, 'Nominal test does not compute')

    def testComputeEnergyWhenBlockedMaximum(self):

        startSector: Coordinates = Coordinates(x=1, y=1)
        endSector:   Coordinates = Coordinates(x=8, y=8)

        expectedStopEnergy: float = 118.99
        decimalPlace:       int   = 2

        stopEnergy: float = self._gameEngine.computeEnergyWhenBlocked(startSector=startSector, endSector=endSector)

        self.logger.info(f'{stopEnergy}')

        self.assertAlmostEqual(expectedStopEnergy, stopEnergy, decimalPlace, 'Maximum case does not compute')

    def testComputeEnergyWhenBlockedMinimum(self):

        startSector: Coordinates = Coordinates(x=1, y=1)
        endSector:   Coordinates = Coordinates(x=1, y=2)

        expectedStopEnergy: float = 30.0
        decimalPlace:       int   = 2

        stopEnergy: float = self._gameEngine.computeEnergyWhenBlocked(startSector=startSector, endSector=endSector)

        self.logger.info(f'{stopEnergy}')

        self.assertAlmostEqual(expectedStopEnergy, stopEnergy, decimalPlace, 'Minimum test does not compute')

    def testComputeCloseCoordinates(self):
        """
        Loop until all directions tested
        """
        testedDirections:  TestedDirections = self._initDirectionTest()
        targetCoordinates: Coordinates      = Coordinates(x=5, y=5)

        while self._areAllDirectionsValidated(testedDirections=testedDirections) is False:

            directionData:     DirectionData = self._gameEngine.computeCloseCoordinates(targetCoordinates=targetCoordinates)

            testedDirections[directionData.direction] = True
            self._validateReturn(targetCoordinates=targetCoordinates, directionData=directionData)

        self.logger.debug(f'All directions tested: {testedDirections=}')

    def testComputeEnergyForWarpTravelMediumDistanceMediumSpeed(self):

        energy: float = self._gameEngine.computeEnergyForWarpTravel(travelDistance=5, warpFactor=5.0)

        self.logger.info(f'{energy=}')

        expectedEnergy: float = 255.05
        decimalPlace:   int   = 2
        self.assertAlmostEqual(expectedEnergy, energy, decimalPlace, 'Nominal test does not compute')

    def testComputeEnergyForWarpTravelMediumDistanceMaximumSpeed(self):

        energy: float = self._gameEngine.computeEnergyForWarpTravel(travelDistance=5, warpFactor=9.9)

        self.logger.info(f'{energy=}')

        expectedEnergy: float = 1945.65
        decimalPlace:   int   = 2
        self.assertAlmostEqual(expectedEnergy, energy, decimalPlace, 'Nominal test does not compute')

    def testComputeEnergyForWarpTravelMediumDistanceMinimumSpeed(self):

        energy: float = self._gameEngine.computeEnergyForWarpTravel(travelDistance=5, warpFactor=1.0)

        self.logger.info(f'{energy=}')

        expectedEnergy: float = 7.05
        decimalPlace:   int   = 2
        self.assertAlmostEqual(expectedEnergy, energy, decimalPlace, 'Nominal test does not compute')

    def testComputeEnergyForWarpTravelMaximumDistanceMediumSpeed(self):

        energy: float = self._gameEngine.computeEnergyForWarpTravel(travelDistance=12, warpFactor=5.0)

        self.logger.info(f'{energy=}')

        expectedEnergy: float = 262.05
        decimalPlace:   int   = 2
        self.assertAlmostEqual(expectedEnergy, energy, decimalPlace, 'Nominal test does not compute')

    def testComputeEnergyForWarpTravelMaximumDistanceMaximumSpeed(self):

        energy: float = self._gameEngine.computeEnergyForWarpTravel(travelDistance=12, warpFactor=9.9)

        self.logger.info(f'{energy=}')

        expectedEnergy: float = 1952.65
        decimalPlace:   int   = 2
        self.assertAlmostEqual(expectedEnergy, energy, decimalPlace, 'Nominal test does not compute')

    def testComputeEnergyForWarpTravelMaximumDistanceMinimumSpeed(self):

        energy: float = self._gameEngine.computeEnergyForWarpTravel(travelDistance=12, warpFactor=1.0)

        self.logger.info(f'{energy=}')

        expectedEnergy: float = 14.05
        decimalPlace:   int   = 2
        self.assertAlmostEqual(expectedEnergy, energy, decimalPlace, 'Nominal test does not compute')

    def _commonComputeHit(self, playerType: PlayerType) -> float:

        self._gameState.playerType = playerType

        shooterPosition: Coordinates = Coordinates(x=7, y=7)
        targetPosition:  Coordinates = Coordinates(x=3, y=7)
        klingonPower:    float       = 348.0

        computedHit = self._gameEngine.computeHit(shooterPosition=shooterPosition,
                                                  targetPosition=targetPosition,
                                                  klingonPower=klingonPower)

        return computedHit

    def _initDirectionTest(self) -> TestedDirections:

        testedDirections: TestedDirections = TestedDirections({})

        for direction in Direction:
            testedDirections[direction] = False

        return testedDirections

    def _validateReturn(self, targetCoordinates: Coordinates, directionData: DirectionData):

        direction:   Direction = directionData.direction
        coordinates: Coordinates = directionData.coordinates
        targetX: int = targetCoordinates.x
        targetY: int = targetCoordinates.y
        newX:    int = coordinates.x
        newY:    int = coordinates.y

        if direction == Direction.North:
            self.assertEqual(newX, targetX, 'X should be unchanged for North')
            self.assertEqual(newY, targetY - 1, 'Y should be less one for North')
        elif direction == Direction.South:
            self.assertEqual(newX, targetX, 'X should be unchanged for South')
            self.assertEqual(newY, targetY + 1, 'Y should be one more for South')
        elif direction == Direction.East:
            self.assertEqual(newX, targetX + 1, 'X should be one more for East')
            self.assertEqual(newY, targetY, 'Y should be unchanged for East')
        elif direction == Direction.West:
            self.assertEqual(newX, targetX - 1, 'X should be one less for West')
            self.assertEqual(newY, targetY, 'Y should be unchanged for West')
        elif direction == Direction.NorthEast:
            self.assertEqual(newX, targetX + 1, 'X should be one 1 more for NorthEast')
            self.assertEqual(newY, targetY - 1, 'Y should be 1 less for NorthEast')
        elif direction == Direction.SouthEast:
            self.assertEqual(newX, targetX + 1, 'X should be one 1 more for SouthEast')
            self.assertEqual(newY, targetY + 1, 'Y should be 1 more for SouthEast')
        elif direction == Direction.NorthWest:
            self.assertEqual(newX, targetX - 1, 'X should be one 1 less for NorthWest')
            self.assertEqual(newY, targetY - 1, 'Y should be 1 less for NorthWest')
        elif direction == Direction.SouthWest:
            self.assertEqual(newX, targetX - 1, 'X should be one 1 less for SouthWest')
            self.assertEqual(newY, targetY + 1, 'Y should be 1 more for SouthWest')

        self.logger.info(f'{direction.name} passed')

    def _areAllDirectionsValidated(self, testedDirections:  TestedDirections) -> bool:
        """

        Args:
            testedDirections: The tested directions dictionary

        Returns: False if at least one entry is True
        """
        for value in testedDirections.values():
            if value is False:
                return False
        return True

    def _runPhaserTest(self, shooterCoordinates: Coordinates, targetCoordinates: Coordinates, expectedPhaserHit: float):

        distance:           float        = self._computer.computeQuadrantDistance(startSector=shooterCoordinates, endSector=targetCoordinates)
        enemyPower:         float       = 500.0
        powerAmount:        float       = 500.0

        phaserHit: float = self._gameEngine.doPhasers(distance=distance, enemyPower=enemyPower, powerAmount=powerAmount)

        self.assertAlmostEqual(expectedPhaserHit, phaserHit, places=1)
        self.logger.info(f'{phaserHit=}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGameEngine))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
