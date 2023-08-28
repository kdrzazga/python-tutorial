from src.sprite import Sprite
from src.constants import Constants

class Karateka(Sprite):

    def __init__(self, x, y):
        super().__init__(x, y, "karateka")
        self.path = "src/resources/k.png"

    def step_right(self):        
        if self.y > Constants.board_limit_x:
            self.disable_move()
        else:
            super().step_right()

    def get_sprite_path(self):
        return "src/resources/k" + self.walk_phase + ".png"
