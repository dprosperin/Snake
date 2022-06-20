from pygame import draw, Rect
from source.settings import *
from source.Fruit import Fruit
from source.Movable import Movable
from source.SnakeBlock import SnakeBlock


class Snake(Movable):
    def __init__(self, nickname: str, color: Color = WHITE,
                 length=5, score=0, **kwargs) -> None:
        super().__init__(**kwargs)
        if kwargs.get('in_game') is not None:
            self.in_game.add_player(self)

        self.position = list(self.position)
        self.color = color
        self.nickname = nickname
        self.score = score
        self.fruit_collected = []
        self.body = []
        self.length = length

    def draw(self):
        if not self.is_hidden and self.in_game:
            for block in self.body:
                draw.rect(self.in_game.surface, self.color,
                          Rect(block.position[0], block.position[1], 10, 10))

    def moving(self):
        if self.is_moving and self.in_game.tick % self.acceleration == 0:
            if self.direction == Snake.UP:
                self.position[1] -= 10
            if self.direction == Snake.DOWN:
                self.position[1] += 10
            if self.direction == Snake.LEFT:
                self.position[0] -= 10
            if self.direction == Snake.RIGHT:
                self.position[0] += 10

            self.body.insert(0, SnakeBlock(color=self.color, position=self.position, direction=self.direction))
            self.body.pop()

    def kill(self):
        self.in_game.players.remove(self)
        super().kill()
        self.length = 0

    def fill_body(self, to_add):
        for x in range(to_add):
            if len(self) == 0:
                self.body.append(SnakeBlock(self.color, direction=self.direction, position=self.position))
            else:
                prev_block = self.body[-1]
                if prev_block.direction == Snake.UP:
                    next_block = SnakeBlock(color=self.color, direction=self.direction,
                                            position=[prev_block.position[0], prev_block.position[1] - 10])
                elif prev_block.direction == Snake.DOWN:
                    next_block = SnakeBlock(color=self.color, direction=self.direction,
                                            position=[prev_block.position[0], prev_block.position[1] + 10])
                elif prev_block.direction == Snake.LEFT:
                    next_block = SnakeBlock(color=self.color, direction=self.direction,
                                            position=[prev_block.position[0] + 10, prev_block.position[1]])
                elif prev_block.direction == Snake.RIGHT:
                    next_block = SnakeBlock(color=self.color, direction=self.direction,
                                            position=[prev_block.position[0] - 10, prev_block.position[1]])
                self.body.append(next_block)

    def cut_body(self, new_length):
        if new_length >= len(self):
            raise ValueError(f"Impossible de découper {new_length} sur {len(self)}")
        self.body = self.body[:new_length]

    def eat(self, fruit: Fruit):
        self.fruit_collected.append(fruit)
        fruit.is_collected = True
        self.give_effects(fruit.give_effects)
        self.in_game.fruits.remove(fruit)

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, new_length: int):
        if not isinstance(new_length, int):
            raise TypeError(f"Un entier positif est attendu mais {type(new_length)} est donnée.")
        if new_length < 0:
            raise ValueError(f"La taille ne peut pas être négative. La valeur {new_length} est donnée.")
        if new_length > len(self):
            self.fill_body(abs(len(self) - new_length))
        elif new_length < len(self):
            self.cut_body(new_length)
        elif new_length == 0:
            self.body = []
        self._length = new_length

    @property
    def positions(self) -> list[tuple[int, int]]:
        return [snake_body_part.position for snake_body_part in self.body]

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        try:
            if new_direction == 'UP' and self._direction != 'DOWN':
                self._direction = 'UP'
            elif new_direction == 'DOWN' and self._direction != 'UP':
                self._direction = 'DOWN'
            elif new_direction == 'LEFT' and self._direction != 'RIGHT':
                self._direction = 'LEFT'
            elif new_direction == 'RIGHT' and self._direction != 'LEFT':
                self._direction = 'RIGHT'
            else:
                self._direction = self._direction
        except AttributeError:
            self._direction = new_direction

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.position}, {self.direction}, {self.nickname}>"

    def __str__(self):
        return f"<{self.__class__.__name__} {self.position}, {self.direction}, {self.nickname}>"

    def __len__(self):
        return len(self.body)
