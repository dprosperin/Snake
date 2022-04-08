import pygame
import time
from pygame.locals import *
from sys import exit

window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
red   = pygame.Color(255, 0, 0)
green = pygame.Color(37, 236, 97)

pygame.init()

pygame.display.set_caption("Position in Pygame")
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

while True: 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    game_window.fill(black)

    pygame.draw.rect(game_window, green, pygame.Rect(100, 10, 20,20))
    pygame.draw.rect(game_window, green, pygame.Rect(100, 100, 20,20))


    pygame.display.update()
    fps.tick(15)