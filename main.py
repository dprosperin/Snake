import pygame
from pygame.locals import QUIT, FULLSCREEN, NOFRAME, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_z, K_q, K_s, K_d, K_SPACE
from source.Game import Game
from source.Snake import Snake
from source.settings import *
from time import time, sleep


class MainActivity:
    def __init__(self, window_resolution: tuple):
        self.window_x, self.window_y = window_resolution
        self.game_window = None
        self.fps = None
        self.finished = None
        self.to_draw = []
        self.round1 = None
        self.player_blue = None
        self.player_red = None

    def handling_score(self, rows):
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

    def init(self):
        pygame.display.set_caption('Snake War v2')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y), flags=FULLSCREEN)
        self.fps = pygame.time.Clock()
        self.finished = False

    def game_loop(self):
        start_time = time()
        while not self.finished:
            self.game_window.fill(BLACK)

            if time() - start_time < 6:
                self.game_window.blit(self.image_rules, (0, 0))

            if 6 < time() - start_time < 12:
                self.game_window.blit(self.image_points, (0, 0))

            if 12 < time() - start_time < 18:
                self.game_window.blit(self.image_fruits, (0, 0))

            if 18 < time() - start_time < 24:
                self.game_window.blit(self.image_key_assignment, (0, 0))

            if time() - start_time > 24 and not self.round1.is_over:
                for draw in self.to_draw:
                    draw()

            if self.round1.is_over:
                self.game_window.fill(BLACK)
                self.scoreboard_screen()
                sleep(5)
                self.finished = True
                exit(0)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.finished = True
                    exit(0)
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.round1.toggle()

                    if event.key == K_UP:
                        self.player_red.direction = Snake.UP
                    if event.key == K_DOWN:
                        self.player_red.direction = Snake.DOWN
                    if event.key == K_LEFT:
                        self.player_red.direction = Snake.LEFT
                    if event.key == K_RIGHT:
                        self.player_red.direction = Snake.RIGHT

                    if event.key == K_z:
                        self.player_blue.direction = Snake.UP
                    if event.key == K_s:
                        self.player_blue.direction = Snake.DOWN
                    if event.key == K_q:
                        self.player_blue.direction = Snake.LEFT
                    if event.key == K_d:
                        self.player_blue.direction = Snake.RIGHT

            # Refresh game screen
            pygame.display.flip()

            # Frame Per Second /Refresh Rate
            self.fps.tick(30)

    def game_setup(self):
        # 1. Affichage des règles
        self.image_rules = pygame.image.load("assets/rules.png").convert()
        self.image_points = pygame.image.load("assets/points.png").convert()
        self.image_fruits = pygame.image.load("assets/fruits.png").convert()
        self.image_key_assignment = pygame.image.load("assets/key_assignment.png").convert()

        # 2. Démarrer la première partie
        self.round1 = Game(self.game_window, self.to_draw)
        self.player_red = Snake("RED", position=(500, 100), color=RED, in_game=self.round1)
        self.player_blue = Snake("BLUE", position=(500, 60), color=BLUE, in_game=self.round1)

        self.round1.spawn_fruits(10)
        self.to_draw.append(self.round1.draw)

    def main(self):
        self.game_setup()
        self.game_loop()


if __name__ == '__main__':
    pygame.init()

    MainActivity.loading_screen()
    screen_resolution = pygame.display.get_desktop_sizes()[0]
    CurrentActivity = MainActivity(screen_resolution)

    CurrentActivity.init()
    CurrentActivity.main()
