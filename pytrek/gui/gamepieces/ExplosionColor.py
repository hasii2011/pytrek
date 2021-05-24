
from enum import Enum


class ExplosionColor(Enum):

    GREY     = 'grey'
    BLUE     = 'blue'
    RED      = 'red'
    WHITE    = 'white'

    __order__ = 'GREY BLUE RED WHITE'
