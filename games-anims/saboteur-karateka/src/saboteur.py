from src.sprite import Sprite

class Saboteur(Sprite):
    
    def __init__(self, x, y):
        super().__init__(x, y, "saboteur")
        self.path = "src/resources/s.png"
    
    def get_sprite_path(self):
        return "src/resources/s" + self.walk_phase + ".png"
