from source.Fruit import Fruit
from pygame import draw, Rect
from source.settings import *


class Lemon(Fruit):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.give_effects = [Lemon.effect_speed_up]

    def draw(self) -> None:
        if not self.is_collected and self.in_game:
            draw.rect(self.in_game.surface, YELLOW, Rect(self.position[0], self.position[1], 10, 10))

    @classmethod
    def effect_speed_up(cls, player) -> bool:
        player.acceleration = max(2, player.acceleration - 7)
        return True
