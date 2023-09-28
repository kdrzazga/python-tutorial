from src.main.sprite import Sprite


class Honda(Sprite):

    def __init__(self, x, y):
        super().__init__(x, y, "honda")
        self.path = "src/main/resources/honda/honda_w2.png"
        self.walk_phase = "w2"
        self.visible = False

    def step_right(self):
        super().step_right()

    def step_left(self):
        super().step_left()

    def get_sprite_path(self):
        return "src/main/resources/honda/honda_" + self.walk_phase + ".png"
