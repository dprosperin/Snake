from matplotlib.pyplot import draw
import pygame


class Snake:
    score = 0
    spawn_position = ()
    speed = 15
    color = red
    lenght = 3  # Blocks
    direction = 'RIGHT'
    body = []

    def __init__(self, surface: pygame.Surface, spawn_position: tuple, color: pygame.Color, speed: int, lenght: int):
        self._surface = surface
        self._spawn_position = spawn_position
        self._color = color
        self._speed = speed

    def draw(self):
        for block in self.body:
            pygame.draw.rect(self.surface, self.color,
                             pygame.Rect(block[0], block[1], 10, 10))
