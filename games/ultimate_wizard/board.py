from player import Player
from enemy import Enemy

class Board:
    
    def __init__(self):
        self.player = Player(0, 0)
        self.enemy = Enemy(50, 50)
        