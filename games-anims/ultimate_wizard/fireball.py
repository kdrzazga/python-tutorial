from bin.sprite import Sprite


class Fireball(Sprite):
    sprite_path = "resources/fb.png"

    def __init__(self, x, y):
        Sprite.__init__(self, x, y, "fireball")

    def get_sprite_path(self):
        return Fireball.sprite_path
