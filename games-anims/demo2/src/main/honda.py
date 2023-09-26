from src.main.sprite import Sprite


class Superfrog(Sprite):

    def __init__(self, x, y):
        super().__init__(x, y, "honda")
        self.path = "src/main/resources/honda/honda1.png"
        self.visible = False

    def step_right(self):
        super().step_right()

    def step_left(self):
        super().step_left()

    def get_sprite_path(self):
        return self.path
