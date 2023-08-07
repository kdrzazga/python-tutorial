from player import Player
from enemy import Enemy

class Board:

    sizeX = 17
    sizeY = 10
    
    def __init__(self):
        self.player = Player(0, 10)
        self.enemy = Enemy(9, 1)
        self.fields = [[0 for _ in range(Board.sizeX)] for _ in range(Board.sizeY)]
        