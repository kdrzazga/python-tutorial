from player import Player
from enemy import Enemy

class Board:

    sizeX = 17
    sizeY = 10

    def __init__(self):
        self.player = Player(16, 9)
        self.enemy = Enemy(9, 3)
    
        self.platforms = []
        
        for x in range(Board.sizeX // 2 - 3):
            self.platforms.append((x, 3))
            
        for x in range(Board.sizeX // 2 - 2, Board.sizeX):
            self.platforms.append((x, 5))
            
        for x in range(Board.sizeX // 5):
            self.platforms.append((x, x + 6))
            self.platforms.append((Board.sizeX - x - 1, x + 6))
        
        for x in range(Board.sizeX):
            self.platforms.append((x, 9))       
            self.platforms.append((x, 1))       
        
        self.ladders = []
        for y in range(Board.sizeY):
            self.ladders.append((3, y))
            self.ladders.append((15, y))

        for y in range(2 * Board.sizeY//3, Board.sizeY):
            self.ladders.append((8, y))
        
        self.fields = [[0 for _ in range(Board.sizeX)] for _ in range(Board.sizeY)] #TODO to be removed
