from Entity import Entity


class Movable(Entity):
    """
    Un objet qui se déplace
    """
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    def __init__(self, direction: 'La direction initiale' = RIGHT, is_moving: bool = True,
                 acceleration: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.direction = direction
        self.is_moving = is_moving
        self.acceleration = acceleration

    def kill(self):
        super().kill()
        self.is_moving = False

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.position}, {self.direction}>"

    def __str__(self):
        return f"<{self.__class__.__name__} {self.position}, {self.direction}>"
