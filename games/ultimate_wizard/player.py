from sprite import Sprite

class Player(Sprite):

    sprite_path = "resources/wizard.png"
    initial_spells = 10

    def __init__(self, x, y):
        Sprite.__init__(self, x, y, "wizard")
        self.score = 0
        self.spells = Player.initial_spells
