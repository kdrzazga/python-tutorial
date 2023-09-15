from src.main.sprite import Sprite


class Karateka(Sprite):

    def __init__(self, x, y, color):
        super().__init__(x, y, "karateka")
        self.color = color
        self.path = "src/main/resources/k.png"

    def step_right(self):
        super().step_right()

    def step_left(self):
        super().step_left()

    def get_sprite_path(self):
        return "src/main/resources/k" + self.walk_phase + ".png"
