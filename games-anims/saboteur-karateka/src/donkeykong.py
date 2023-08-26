from src.sprite import Sprite

class DonkeyKong(Sprite):

    def __init__(self):
        x = 920
        y = 330
        super().__init__(x, y, "donkey kong")
        self.walk_phase = 'w2'
        self.path = "src/resources/dkw2.png"


    def turn_left(self):
        self.walk_phase = 'w1'


    def turn_right(self):
        self.walk_phase = 'w2'


    def get_sprite_path(self):
        return "src/resources/dk" + self.walk_phase + ".png"
