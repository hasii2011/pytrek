
from unittest import TestResult
from unittest import TestLoader
from unittest import TextTestRunner

from unittest.suite import TestSuite

# from tests.ComputerTest import ComputerTest
# from tests.CoordinateTest import CoordinateTest
# from tests.ExplosionColorTest import ExplosionColorTest
from pytrek.settings.SettingsCommon import SettingsCommon
from tests.TestComputer import TestComputer
from tests.TestQuadrant import TestQuadrant
from tests.TestIntelligence import TestIntelligence
from tests.TestSmoothMotion import TestSmoothMotion
from tests.TestGameState import TestGameState

from tests.pytrek.settings.TestGameSettings import TestGameSettings

from tests.pytrek.engine.TestGameEngine import TestGameEngine

from tests.pytrek.model.TestGalaxy import TestGalaxy


def createTestSuite() -> TestSuite:
    #
    # Because of the way the unit test debug logging is set up the test runner needs to run
    # from the project working directory
    #
    # Initialize the test suite
    loader: TestLoader = TestLoader()
    testSuite:  TestSuite  = TestSuite()

    # add tests to the suite
    # testSuite.addTest(loader.loadTestsFromTestCase(ComputerTest))
    # testSuite.addTest(loader.loadTestsFromTestCase(CoordinateTest))
    # testSuite.addTest(loader.loadTestsFromTestCase(ExplosionColorTest))
    # testSuite.addTest(loader.loadTestsFromTestCase(GameEngineTest))
    # testSuite.addTest(loader.loadTestsFromTestCase(GameStatisticsTest))
    testSuite.addTest(loader.loadTestsFromTestCase(TestIntelligence))
    testSuite.addTest(loader.loadTestsFromTestCase(TestComputer))
    testSuite.addTest(loader.loadTestsFromTestCase(TestQuadrant))
    testSuite.addTest(loader.loadTestsFromTestCase(TestQuadrant))
    testSuite.addTest(loader.loadTestsFromTestCase(TestSmoothMotion))
    testSuite.addTest(loader.loadTestsFromTestCase(TestGameState))
    testSuite.addTest(loader.loadTestsFromTestCase(TestGameSettings))
    testSuite.addTest(loader.loadTestsFromTestCase(TestGameEngine))
    testSuite.addTest(loader.loadTestsFromTestCase(TestGalaxy))

    return testSuite


def main():

    SettingsCommon.determineSettingsLocation()

    testSuite: TestSuite      = createTestSuite()
    runner:    TextTestRunner = TextTestRunner(verbosity=2)
    result:    TestResult     = runner.run(testSuite)

    print(f"The molon labe results are in\n{result}")


if __name__ == "__main__":
    main()
