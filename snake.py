# importing libraries
import csv
import pygame
import time
import random
from pygame.locals import FULLSCREEN, KEYDOWN, QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_z, K_q, K_s, K_d

# Initialising pygame
pygame.init()

snake_speed = 25

# Window size
screen_resolution = pygame.display.get_desktop_sizes()[0]
window_x, window_y = screen_resolution

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialise game window
pygame.display.set_caption('Snake version 1')
game_window = pygame.display.set_mode((window_x, window_y), flags=FULLSCREEN)

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
red_snake_position = [0, 50]
blue_snake_position = [0, window_y - 20]

blue_snake_size = 10
red_snake_size = 10

# defining first 4 blocks of snake body
blue_snake_body = [[x, blue_snake_position[1]] for x in range(
    blue_snake_position[0], blue_snake_position[0] - red_snake_size * 10, -10)]
red_snake_body = [[x, red_snake_position[1]] for x in range(
    red_snake_position[0], red_snake_position[0] - blue_snake_size * 10, -10)]

# fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True

# setting default snake direction towards
# right
blue_snake_direction = 'RIGHT'
blue_change_to = blue_snake_direction

red_snake_direction = 'RIGHT'
red_snake_change_to = red_snake_direction

# initial score
blue_snake_score = 0
red_snake_score = 0


def write_score(score: int, player: str, score_path='./score.csv') -> None:
    """Sauvegarde le score d'un joueur"""
    with open(score_path, mode='a', encoding='utf-8', newline='') as score_file:
        fieldnames = ['player', 'score']
        writer = csv.DictWriter(score_file, fieldnames=fieldnames)
        writer.writerow(
            {'player': player, 'score': score})


def read_score(handling, score_path='./score.csv'):
    """Lit les scores des joueurs"""
    with open(score_path, mode='r', encoding='utf-8', newline='') as score_file:
        handling(csv.DictReader(score_file))


# displaying Score function
def show_score(score: int, left: int, font_size: int = 20,
               font_color: pygame.Color = pygame.Color(255, 255, 255)) -> pygame.Rect:
    # creating font object score_font
    score_font = pygame.font.Font('./fonts/Gameplay.ttf', font_size)

    # create the display surface object
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, font_color)

    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()
    score_rect.left = left

    # displaying text
    game_window.blit(score_surface, score_rect)

    return score_rect


# game over function
def game_over():
    global blue_snake_score
    global red_snake_score

    game_window.fill(black)

    # creating font object my_font
    my_font = pygame.font.Font('./fonts/Gameplay.ttf', 40)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render(
        'Blue score is : ' + str(blue_snake_score), True, blue)

    game_over_surface2 = my_font.render(
        'Red score is : ' + str(red_snake_score), True, red)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()
    game_over_rect2 = game_over_surface2.get_rect()

    # setting position of the text
    game_over_rect.midtop = (window_x / 4, window_y / 4)
    game_over_rect2.midtop = (window_x / 1.5, window_y / 4)

    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    game_window.blit(game_over_surface2, game_over_rect2)
    pygame.display.flip()

    write_score(player="red", score=red_snake_score)
    write_score(player="blue", score=blue_snake_score)

    time.sleep(2)

    # Display previous score
    my_text = pygame.font.Font('./fonts/Gameplay.ttf', 20)

    pygame.display.update()

    # Show saved score
    def handling_score(rows):
        game_window.fill(black)
        score_headers = 'Score  Name'

        score_headers_surface = my_font.render(score_headers, True, white)
        score_headers_rect = score_headers_surface.get_rect()
        score_headers_rect.midtop = (window_x / 2, window_y / 4)
        game_window.blit(score_headers_surface, score_headers_rect)

        top_position = score_headers_rect.top + score_headers_rect.height + 5

        def sort_score(row: dict) -> str:
            return row.get("score")

        best_score = list(rows)

        best_score.sort(key=sort_score, reverse=True)

        for row in best_score[0:5]:
            current_score_text = '{score:03d}    {player}'.format(score=int(row['score']),
                                                                  player=row['player'])
            current_score_surface = my_text.render(current_score_text, True, white)
            current_score_rect = current_score_surface.get_rect()
            current_score_rect.midtop = (window_x / 2, top_position)

            game_window.blit(current_score_surface, current_score_rect)
            pygame.display.update()
            top_position += current_score_rect.height
            if top_position >= window_y:
                break

        game_window.fill(black)

    read_score(handling_score)

    # after 2 seconds we will quit the program
    time.sleep(5)

    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


done = False

# Main Function
while not done:

    # handling key events
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_UP:
                blue_change_to = 'UP'
            if event.key == K_DOWN:
                blue_change_to = 'DOWN'
            if event.key == K_LEFT:
                blue_change_to = 'LEFT'
            if event.key == K_RIGHT:
                blue_change_to = 'RIGHT'

            if event.key == K_z:
                red_snake_change_to = 'UP'
            if event.key == K_s:
                red_snake_change_to = 'DOWN'
            if event.key == K_q:
                red_snake_change_to = 'LEFT'
            if event.key == K_d:
                red_snake_change_to = 'RIGHT'

    # If two keys pressed simultaneously
    # we don't want snake to move into two
    # directions simultaneously
    if blue_change_to == 'UP' and blue_snake_direction != 'DOWN':
        blue_snake_direction = 'UP'
    if blue_change_to == 'DOWN' and blue_snake_direction != 'UP':
        blue_snake_direction = 'DOWN'
    if blue_change_to == 'LEFT' and blue_snake_direction != 'RIGHT':
        blue_snake_direction = 'LEFT'
    if blue_change_to == 'RIGHT' and blue_snake_direction != 'LEFT':
        blue_snake_direction = 'RIGHT'

    if red_snake_change_to == 'UP' and red_snake_direction != 'DOWN':
        red_snake_direction = 'UP'
    if red_snake_change_to == 'DOWN' and red_snake_direction != 'UP':
        red_snake_direction = 'DOWN'
    if red_snake_change_to == 'LEFT' and red_snake_direction != 'RIGHT':
        red_snake_direction = 'LEFT'
    if red_snake_change_to == 'RIGHT' and red_snake_direction != 'LEFT':
        red_snake_direction = 'RIGHT'

    # Moving the snake
    if blue_snake_direction == 'UP':
        blue_snake_position[1] -= 10
    if blue_snake_direction == 'DOWN':
        blue_snake_position[1] += 10
    if blue_snake_direction == 'LEFT':
        blue_snake_position[0] -= 10
    if blue_snake_direction == 'RIGHT':
        blue_snake_position[0] += 10

    # Moving the snake
    if red_snake_direction == 'UP':
        red_snake_position[1] -= 10
    if red_snake_direction == 'DOWN':
        red_snake_position[1] += 10
    if red_snake_direction == 'LEFT':
        red_snake_position[0] -= 10
    if red_snake_direction == 'RIGHT':
        red_snake_position[0] += 10

    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    blue_snake_body.insert(0, list(blue_snake_position))

    red_snake_body.insert(0, list(red_snake_position))

    if blue_snake_position[0] == fruit_position[0] and blue_snake_position[1] == fruit_position[1]:
        blue_snake_score += 10
        fruit_spawn = False
    else:
        blue_snake_body.pop()

    if red_snake_position[0] == fruit_position[0] and red_snake_position[1] == fruit_position[1]:
        red_snake_score += 10
        fruit_spawn = False
    else:
        red_snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True
    game_window.fill(black)

    for pos in blue_snake_body:
        pygame.draw.rect(game_window, blue,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    for pos in red_snake_body:
        pygame.draw.rect(game_window, red,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if blue_snake_position[0] < 0 or blue_snake_position[0] > window_x - 10:
        game_over()
    if blue_snake_position[1] < 0 or blue_snake_position[1] > window_y - 10:
        game_over()

    if red_snake_position[0] < 0 or red_snake_position[0] > window_x - 10:
        game_over()
    if red_snake_position[1] < 0 or red_snake_position[1] > window_y - 10:
        game_over()

        # Touching the snake body
    for block in blue_snake_body[1:]:
        if (blue_snake_position[0] == block[0] and blue_snake_position[1] == block[1]) or (
                red_snake_position[0] == block[0] and red_snake_position[1] == block[1]):
            game_over()

    for block in red_snake_body[1:]:
        if (blue_snake_position[0] == block[0] and blue_snake_position[1] == block[1]) or (
                red_snake_position[0] == block[0] and red_snake_position[1] == block[1]):
            game_over()

    # displaying score countinuously
    blue_snake_score_Rect = show_score(blue_snake_score, 10, font_color=blue)
    left_position_red_score = blue_snake_score_Rect.left + blue_snake_score_Rect.width + 10
    show_score(red_snake_score, left_position_red_score, font_color=red)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
