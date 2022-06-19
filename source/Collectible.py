from source.Entity import Entity


class Collectible(Entity):

    def __init__(self, is_collected: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.is_collected = is_collected
        self.is_hidden = not is_collected
