from source.Movable import Movable
from pygame.color import Color
from copy import deepcopy


class SnakeBlock(Movable):
    def __init__(self, color: Color, **kwargs):
        super().__init__(**kwargs)
        self.position = deepcopy(kwargs.get('position'))
