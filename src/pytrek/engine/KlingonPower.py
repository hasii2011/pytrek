from enum import Enum


class KlingonPower(Enum):
    """"
    Attacker Initial energy levels (nominal):
              Klingon   Romulan   Commander   Super-Commander
     Novice    400        700        1200
     Fair      425        750        1250
     Good      450        800        1300        1750
     Expert    475        850        1350        1875
     Emeritus  500        900        1400        2000
    """
    Novice   = 400
    Fair     = 425
    Good     = 450
    Expert   = 475
    Emeritus = 500
