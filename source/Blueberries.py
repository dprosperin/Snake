from source.Fruit import Fruit
from pygame import draw, Rect
from settings import *


class Blueberries(Fruit):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.give_effects = [Blueberries.effect_suicide]

    def draw(self) -> None:
        if not self.is_collected and self.in_game:
            draw.rect(self.in_game.surface, BLUE, Rect(self.position[0], self.position[1], 10, 10))

    @classmethod
    def effect_suicide(cls, player) -> bool:
        player.kill()
        return True
