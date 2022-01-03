
from tests.LogMessageConsole import LogMessageConsole

from tests.TestBase import TestBase

TestBase.setUpLogging()

pmc: LogMessageConsole = LogMessageConsole()

print(f'{id(pmc)=}')

pmc.displayMessage("Print this sucker")

pmc = LogMessageConsole()

print(f'{id(pmc)=}')
