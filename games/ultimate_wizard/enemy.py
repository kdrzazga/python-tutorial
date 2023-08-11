from sprite import Sprite

class Enemy(Sprite):

    sprite_path = "resources/knight.png"
    tobmstone_path = "resources/tombstone.png"

    def __init__(self, x, y):
        Sprite.__init__(self, x, y, "knight")

    def get_sprite_path(self):
        return Enemy.sprite_path if self.active else Enemy.tobmstone_path
