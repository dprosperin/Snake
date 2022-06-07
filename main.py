import pygame
from pygame.locals import QUIT, FULLSCREEN, NOFRAME, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_z, K_q, K_s, K_d, K_SPACE
from source.Game import Game
from source.Snake import Snake
from source.Cherry import Cherry
from source.Lemon import Lemon
from source.Lime import Lime
from source.Blueberries import Blueberries
from source.settings import *


class MainActivity:
    def __init__(self, window_resolution: tuple):
        self.window_x, self.window_y = window_resolution
        self.game_window = None

    def handling_score(self, rows):
        # self.game_window.fill(black)
        score_headers = 'Top scores'

        score_headers_surface = HEADING.render(score_headers, True, WHITE)
        score_headers_rect = score_headers_surface.get_rect()
        score_headers_rect.midtop = (self.window_x / 2, self.window_y / 4)
        self.game_window.blit(score_headers_surface, score_headers_rect)

        top_position = score_headers_rect.top + score_headers_rect.height + 5

        def sort_score(row: dict) -> str:
            return row.get("score")

        best_score = list(rows)

        best_score.sort(key=sort_score, reverse=True)

        for row in best_score[0:5]:
            current_score_text = '{score:03d}    {player}'.format(score=int(row['score']),
                                                                  player=row['player'])
            current_score_surface = TEXT.render(current_score_text, True, WHITE)
            current_score_rect = current_score_surface.get_rect()
            current_score_rect.midtop = (self.window_x / 2, top_position)

            self.game_window.blit(current_score_surface, current_score_rect)
            pygame.display.flip()
            top_position += current_score_rect.height
            if top_position >= self.window_y:
                break

        self.game_window.fill(BLACK)

    def scoreboard_screen(self):
        Game.read_score(self.handling_score)

    def rules_screen(self):
        pass

    @staticmethod
    def loading_screen():
        window_x = 300
        window_y = 200

        loading_window = pygame.display.set_mode((window_x, window_y), flags=NOFRAME)
        loading_window.fill(BLACK)

        title_surface = LOGO.render('Snake', True, WHITE)
        title_rect = title_surface.get_rect()
        title_rect.midtop = (window_x / 2, window_y / 3)

        loading_window.blit(title_surface, title_rect)
        pygame.display.flip()
        pygame.time.delay(5000)

    def main(self):
        pygame.display.set_caption('Snake v1.1')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y), flags=FULLSCREEN)

        fps = pygame.time.Clock()

        finished = False

        round1 = Game(self.game_window)
        fruit1 = Lime(in_game=round1, position=[50, 100])
        fruit2 = Lemon(in_game=round1, position=[100, 200])
        fruit3 = Blueberries(in_game=round1, position=[160, 300])
        fruit4 = Cherry(in_game=round1, position=[160, 400])
        player_red = Snake("RED", position=(500, 100), color=RED, in_game=round1)
        player_blue = Snake("BLUE", position=(500, 70), color=BLUE, in_game=round1)

        round1.start()

        while not finished:
            self.game_window.fill(BLACK)

            for event in pygame.event.get():
                if event.type == QUIT:
                    finished = True
                    exit(0)
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        round1.toggle()

                    if event.key == K_UP:
                        player_red.direction = Snake.UP
                    if event.key == K_DOWN:
                        player_red.direction = Snake.DOWN
                    if event.key == K_LEFT:
                        player_red.direction = Snake.LEFT
                    if event.key == K_RIGHT:
                        player_red.direction = Snake.RIGHT

                    if event.key == K_z:
                        player_blue.direction = Snake.UP
                    if event.key == K_s:
                        player_blue.direction = Snake.DOWN
                    if event.key == K_q:
                        player_blue.direction = Snake.LEFT
                    if event.key == K_d:
                        player_blue.direction = Snake.RIGHT

            round1.draw()

            # Refresh game screen
            pygame.display.flip()

            # Frame Per Second /Refresh Rate
            fps.tick(30)



if __name__ == '__main__':
    pygame.init()

    MainActivity.loading_screen()
    screen_resolution = pygame.display.get_desktop_sizes()[0]
    CurrentActivity = MainActivity(screen_resolution)

    CurrentActivity.main()
