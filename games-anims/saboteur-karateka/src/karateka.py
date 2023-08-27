from src.sprite import Sprite


class Karateka(Sprite):

    def __init__(self, x, y):
        super().__init__(x, y, "karateka")
        self.path = "src/resources/k.png"

    def get_sprite_path(self):
        return "src/resources/k" + self.walk_phase + ".png"
