from sprite import Sprite

class Player(Sprite):

    sprite_path = "resources/wizard.png"
    tobmstone_path = "resources/tombstone2.png"
    initial_spells = 20

    def __init__(self, x, y):
        Sprite.__init__(self, x, y, "wizard")
        self.score = 0
        self.energy = 6
        self.spells = Player.initial_spells
    
    def get_sprite_path(self):
        return Player.sprite_path if self.energy > 0 else Player.tobmstone_path
