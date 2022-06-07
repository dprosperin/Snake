from source.Fruit import Fruit
from pygame import draw, Rect
from settings import *


class Lime(Fruit):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.give_effects = [Lime.effect_speed_down]

    def draw(self) -> None:
        if not self.is_collected and self.in_game:
            draw.rect(self.in_game.surface, GREEN, Rect(self.position[0], self.position[1], 10, 10))

    @classmethod
    def effect_speed_down(cls, player) -> bool:
        player.acceleration = max(2, player.acceleration + 0.75)
        return True
