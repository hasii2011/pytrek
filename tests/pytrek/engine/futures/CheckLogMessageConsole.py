
from pytrek.gui.LogMessageConsole import LogMessageConsole

from tests.TestBase import TestBase

TestBase.setUpClass()

pmc: LogMessageConsole = LogMessageConsole()

print(f'{id(pmc)=}')

pmc.displayMessage("Print this sucker")

pmc = LogMessageConsole()

print(f'{id(pmc)=}')
