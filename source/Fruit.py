from source.Collectible import Collectible
from pygame import draw, Rect
from source.settings import *


class Fruit(Collectible):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if kwargs.get('in_game') is not None:
            self.in_game.add_fruit(self)

        self.give_effects = []

    def draw(self) -> None:
        if not self.is_collected and self.in_game:
            draw.rect(self.in_game.surface, RED, Rect(self.position[0], self.position[1], 10, 10))


