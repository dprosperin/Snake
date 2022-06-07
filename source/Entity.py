from Alterable import Alterable


class Entity(Alterable):
    """Un objet dans le jeu"""

    def __init__(self, in_game=None, position: tuple[int, int] = (0, 0), is_hidden: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.in_game = in_game
        self.position = position
        self.is_hidden = is_hidden
        if in_game is not None:
            self.spawn(in_game)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.position}>"

    def __str__(self):
        return f"<{self.__class__.__name__} {self.position}>"

    def spawn(self, in_game):
        self.in_game = in_game
        self.is_hidden = False

    def kill(self):
        self.position = None
        self.is_hidden = True
        self.in_game = None
