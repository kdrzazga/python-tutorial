from sprite import Sprite

class Enemy(Sprite):

    sprite_path = "resources/knight.png"

    def __init__(self, x, y):
        self.x = x
        self.y = y
