
from logging import Logger
from logging import getLogger


class FutureEventHandlers:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def superNovaEventHandler(self):
        self.logger.warning(f'SuperNova handler fired but am doing Nada')

    def tractorBeamEventHandler(self):
        self.logger.warning(f'TractorBeam fired but am doing Nada')

    def commanderAttacksBaseEventHandler(self):
        self.logger.warning(f'CommanderAttacksBase fired but am doing Nada')
