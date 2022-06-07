class Alterable:
    def __init__(self, effects=None):
        if effects is None:
            effects = []
        self.effects = effects

    def give_effects(self, new_effects) -> None:
        self.effects.extend(new_effects)

    def apply_effects(self) -> None:
        for effect in self.effects:
            result = effect(self)
            if result:
                self.effects.remove(effect)

    def clear_effects(self) -> None:
        self.effects = []

    def add_effect(self, new_effect) -> None:
        self.effects.append(new_effect)
