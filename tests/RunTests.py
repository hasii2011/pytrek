
from unittest import TestResult
from unittest import TestLoader
from unittest import TextTestRunner

from unittest.suite import TestSuite

# from tests.ComputerTest import ComputerTest
# from tests.CoordinateTest import CoordinateTest
# from tests.ExplosionColorTest import ExplosionColorTest
# from tests.GameEngineTest import GameEngineTest
# from tests.GameStatisticsTest import GameStatisticsTest
from tests.TestComputer import TestComputer
from tests.TestQuadrant import TestQuadrant
# from tests.SettingsTest import SettingsTest
from tests.TestIntelligence import TestIntelligence
# from tests.KlingonPowerTest import KlingonPowerTest


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
    # testSuite.addTest(loader.loadTestsFromTestCase(SettingsTest))

    return testSuite


def main():

    testSuite: TestSuite      = createTestSuite()
    runner:    TextTestRunner = TextTestRunner(verbosity=2)
    result:    TestResult     = runner.run(testSuite)

    print(f"THE RESULTS ARE IN\n{result}")


if __name__ == "__main__":
    main()
