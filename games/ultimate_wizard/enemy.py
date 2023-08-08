from sprite import Sprite

class Enemy(Sprite):

    sprite_path = "resources/knight.png"

    def __init__(self, x, y):
        Sprite.__init__(self, x, y)
