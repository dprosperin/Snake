# importing libraries
import csv
import pygame
import time
import random
import datetime
import json
import os
import sys

snake_speed = 15

# Window size
window_x = 1080
window_y = 720

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('GeeksforGeeks Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position2 = [100, 50]
snake_position = [500, 50]
size2 = 10
size = 10


# defining first 4 blocks of snake body
"""snake_body2 = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

snake_body = [[500, 50],
              [490, 50],
              [480, 50],
              [470, 50]
              ]"""

snake_body = [[x, 50] for x in range(
    snake_position[0], snake_position[0] - size * 10, -10)]
snake_body2 = [[x, 50] for x in range(
    snake_position2[0], snake_position2[0] - size2 * 10, -10)]

# fruit position
fruit_position = [random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

direction2 = 'RIGHT'
change_to2 = direction

# initial score
score = 0
score2 = 0


def write_score(score: int, player: str, score_path='./score.csv'):
    """Sauvegarde le score d'un joueur"""
    with open(score_path, mode='a', encoding='utf-8', newline='') as score_file:
        fieldnames = ['datetime', 'player', 'score']
        writer = csv.DictWriter(score_file, fieldnames=fieldnames)

        # writer.writeheader()
        writer.writerow(
            {'datetime': datetime.datetime.today(), 'player': player, 'score': score})


def read_score(score_path='./score.csv'):
    """Lit les scores des joueurs"""
    with open(score_path, mode='r', encoding='utf-8') as score_file:
        return csv.DictReader(score_file)

# displaying Score function


def show_score(choice, color, size, myscore, left):

    # creating font object score_font
    score_font = pygame.font.Font('./fonts/Gameplay.ttf', size)

    # create the display surface object
    # score_surface
    score_surface = score_font.render('Score : ' + str(myscore), True, color)

    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()
    score_rect.left = left

    # displaying text
    game_window.blit(score_surface, score_rect)

# game over function


def game_over(score, score2):

    # creating font object my_font
    #my_font = pygame.font.SysFont('arial', 50)
    my_font = pygame.font.Font('./fonts/Gameplay.ttf', 40)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, blue)

    game_over_surface2 = my_font.render(
        'Your Score is : ' + str(score2), True, red)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()
    game_over_rect2 = game_over_surface2.get_rect()

    # setting position of the text
    game_over_rect.midtop = (window_x/4, window_y/4)
    game_over_rect2.midtop = (window_x/1.5, window_y/4)

    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    game_window.blit(game_over_surface2, game_over_rect2)
    pygame.display.flip()

    # after 2 seconds we will quit the program
    time.sleep(2)

    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


# Main Function
while True:

    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

            if event.key == pygame.K_z:
                change_to2 = 'UP'
            if event.key == pygame.K_s:
                change_to2 = 'DOWN'
            if event.key == pygame.K_q:
                change_to2 = 'LEFT'
            if event.key == pygame.K_d:
                change_to2 = 'RIGHT'

    # If two keys pressed simultaneously
    # we don't want snake to move into two
    # directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if change_to2 == 'UP' and direction2 != 'DOWN':
        direction2 = 'UP'
    if change_to2 == 'DOWN' and direction2 != 'UP':
        direction2 = 'DOWN'
    if change_to2 == 'LEFT' and direction2 != 'RIGHT':
        direction2 = 'LEFT'
    if change_to2 == 'RIGHT' and direction2 != 'LEFT':
        direction2 = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Moving the snake
    if direction2 == 'UP':
        snake_position2[1] -= 10
    if direction2 == 'DOWN':
        snake_position2[1] += 10
    if direction2 == 'LEFT':
        snake_position2[0] -= 10
    if direction2 == 'RIGHT':
        snake_position2[0] += 10

    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    snake_body.insert(0, list(snake_position))
    snake_body2.insert(0, list(snake_position2))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if snake_position2[0] == fruit_position[0] and snake_position2[1] == fruit_position[1]:
        score2 += 10
        fruit_spawn = False
    else:
        snake_body2.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                          random.randrange(1, (window_y//10)) * 10]

    fruit_spawn = True
    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, blue,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    for pos in snake_body2:
        pygame.draw.rect(game_window, red,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        pass
        #game_over(score, score2)
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        pass
        #game_over(score, score2)

    if snake_position2[0] < 0 or snake_position2[0] > window_x-10:
        pass
        #game_over(score, score2)
    if snake_position2[1] < 0 or snake_position2[1] > window_y-10:
        pass
        #game_over(score, score2)

        # Touching the snake body
    for block in snake_body[1:]:
        if (snake_position[0] == block[0] and snake_position[1] == block[1]) or (snake_position2[0] == block[0] and snake_position2[1] == block[1]):
            write_score(player='red',
                        score=score)
            print(dir(read_score()))

            #game_over(score, score2)

    for block in snake_body2[1:]:
        if (snake_position[0] == block[0] and snake_position[1] == block[1]) or (snake_position2[0] == block[0] and snake_position2[1] == block[1]):
            write_score(player='blue',
                        score=score2)
            print(dir(read_score()))
            #game_over(score, score2)

    # displaying score countinuously
    show_score(1, blue, 20, score, 0)
    show_score(1, red, 20, score2, 120)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
