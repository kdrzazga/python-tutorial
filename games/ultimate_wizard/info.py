from player import Player

class Info:

    def __init__(self):
        self.title = "ULTIMATE WIZARD"
        self.score = 0
        self.spells = Player.initial_spells
        
    def update(self, score, spells):
        self.score = score
        self.spells = spells
