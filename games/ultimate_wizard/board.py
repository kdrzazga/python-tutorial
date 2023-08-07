from player import Player
from enemy import Enemy

class Board:

    sizeX = 17
    sizeY = 10
    
    def __init__(self):
        self.player = Player(16, 9)
        self.enemy = Enemy(9, 3)
        self.platforms = [(0,3), (1,3), (2,3), (3,3), (0,9), (1,9), (2,9), (3,9), (4,9), (5,9), (6,9), (8,9), (9,9), (14,9), (15,9), (16,9)]
        self.fields = [[0 for _ in range(Board.sizeX)] for _ in range(Board.sizeY)]
        