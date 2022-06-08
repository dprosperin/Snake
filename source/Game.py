import csv
from pygame import Surface
from source.Fruit import Fruit
import settings
from source.Snake import Snake
from Cherry import Cherry
from Lemon import Lemon
from Lime import Lime
from Blueberries import Blueberries
from random import randint


class Game:
    """Représente une partie de jeu"""

    def __init__(self, surface: Surface, to_draw, is_score_shown: bool = True) -> None:
        self.surface = surface
        self.players = []
        self.fruits = []
        self.is_over = False
        self.is_score_shown = is_score_shown
        self.tick = 0
        self.is_paused = True
        self.to_draw = to_draw

    def start(self) -> None:
        """Démarre la partie"""
        for player in self.players:
            player.spawn(self)

    def pause(self) -> None:
        """Met la partie sur pause"""
        for player in self.players:
            player.is_moving = False
        self.is_paused = True
        print("La partie est sur pause.")

    def play(self) -> None:
        """Reprend la partie"""
        for player in self.players:
            player.is_moving = True
        self.is_paused = False
        print("La partie reprend")

    def toggle(self) -> None:
        if self.is_paused:
            self.play()
        else:
            self.pause()

    def add_player(self, player: Snake) -> None:
        """Ajout un joueur"""
        if isinstance(player, Snake):
            self.players.append(player)
        else:
            raise ValueError("Player n'est pas un Snake")

    def add_fruit(self, fruit: Fruit) -> None:
        """Ajout un joueur"""
        if isinstance(fruit, Fruit):
            self.fruits.append(fruit)
        else:
            raise ValueError("fruit n'est pas un Fruit")

    def kill_players(self) -> None:
        for player in self.players:
            player.kill()

    def spawn_fruits(self, number_of_fruits):
        fruits_existing = [Cherry, Lemon, Lime, Blueberries]
        x, y = self.surface.get_size()
        for i in range(number_of_fruits):
            fruit_to_add = fruits_existing[randint(0, 3)]
            fruit_position = [randint(0, x), randint(0, y)]
            while fruit_position in [element.position for element in self.game_set]:
                fruit_position = [randint(0, x), randint(0, y)]
            self.fruits.append(fruit_to_add(in_game=self, position=fruit_position))

    def clear_fruits(self) -> None:
        for fruit in self.fruits:
            fruit.kill()

    def over(self, is_save: bool = True) -> None:
        """Termine la partie"""
        if is_save:
            self.save()
        self.kill_players()
        self.clear_fruits()
        self.is_over = True
        self.to_draw = []
        print("La partie est terminée !")

    def save(self):
        """Sauvegarde la partie"""
        for player in self.players:
            Game.save_score(player)

    def draw(self):
        if not self.is_over:
            self.tick += 1

            self.check_collisions()
            self.apply_players_effects()

            for player in self.players:
                player.moving()
                player.draw()

            for fruit in self.fruits:
                fruit.draw()

            if self.is_score_shown:
                self.show_score()

    def apply_players_effects(self):
        for player in self.players:
            player.apply_effects()

    def check_border_collisions(self):
        window_x = self.surface.get_width()
        window_y = self.surface.get_height()

        for player in self.players:
            player_x, player_y = player.position
            if player_x < 0 or player_x > window_x - 10:
                self.over()
            if player_y < 0 or player_y > window_y - 10:
                self.over()

    def check_players_collisions(self):
        for player in self.players:
            for body in player.positions[1:]:
                if player.position == body:
                    self.over()

        for current_player in self.players:
            other_players = set(self.players) - {current_player}
            for block in current_player.positions:
                for other_player in other_players:
                    if block in other_player.positions:
                        self.over()

    def check_fruit_collisions(self):
        for player in self.players:
            for fruit in self.fruits:
                if player.position == fruit.position:
                    player.eat(fruit)
                    self.spawn_fruits(1)

    def check_collisions(self):
        self.check_border_collisions()
        self.check_players_collisions()
        self.check_fruit_collisions()

    @staticmethod
    def save_score(player: Snake, score_path='./score.csv') -> None:
        """Sauvegarde le score d'un joueur"""
        with open(score_path, mode='a', encoding='utf-8', newline='') as score_file:
            fieldnames = ['player', 'score']
            writer = csv.DictWriter(score_file, fieldnames=fieldnames)

            writer.writerow(
                {'player': player.nickname, 'score': player.score})

    @staticmethod
    def read_score(handling: 'Callback function', score_path='./score.csv') -> None:
        """Lit les scores des joueurs"""
        with open(score_path, mode='r', encoding='utf-8', newline='') as score_file:
            handling(csv.DictReader(score_file))

    @staticmethod
    def show_scoreboard(self) -> None:
        """Affiche le tableau des scores."""
        pass

    def show_score(self) -> None:
        """displaying score countinuously"""
        for player in self.players:
            score_surface = settings.HEADING.render(str(player.score), True, player.color)

            score_rect = score_surface.get_rect()
            score_rect.x = player.position[0] - 10

            score_rect.y = 10

            # displaying text
            self.surface.blit(score_surface, score_rect)

    @property
    def game_set(self):
        game_set = self.players.copy()
        game_set.extend(self.fruits.copy())
        return game_set
