
from pytrek.gui.LogMessageConsole import LogMessageConsole

from tests.ProjectTestBase import ProjectTestBase

ProjectTestBase.setUpClass()

pmc: LogMessageConsole = LogMessageConsole()

print(f'{id(pmc)=}')

pmc.displayMessage("Print this sucker")

pmc = LogMessageConsole()

print(f'{id(pmc)=}')
