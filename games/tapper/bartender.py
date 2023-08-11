import logging

from sprite import Sprite

class Player(Sprite):

    sprite_path = "resources/tapper-counter.png"
    bar_sprite_path = "resources/tapper-bar.png"

    def __init__(self):
        x = 0
        y = 0
        Sprite.__init__(self, x, y, "bardender")
        self.score = 0
        self.slot = 1
        self.status = 'counter'
        self.status_bitmap_dict = {'counter' : Player.sprite_path, 'bar' : Player.bar_sprite_path}
    
    def get_sprite_path(self):
        return self.status_bitmap_dict[self.status]

    def set_status(self, new_status):
        self.status = new_status
