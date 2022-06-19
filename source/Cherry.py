from source.Fruit import Fruit
from pygame import draw, Rect
from source.settings import *


class Cherry(Fruit):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.give_effects = [Cherry.effect_add_score, Cherry.effect_add_length]

    def draw(self) -> None:
        if not self.is_collected and self.in_game:
            draw.rect(self.in_game.surface, RED, Rect(self.position[0], self.position[1], 10, 10))

    @classmethod
    def effect_add_score(cls, player) -> bool:
        player.score += 10
        return True

    @classmethod
    def effect_add_length(cls, player) -> bool:
        player.length += 1
        return True
