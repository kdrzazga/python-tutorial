import logging

from player import Player
from enemy import Enemy

class Board:

    sizeX = 17
    sizeY = 10

    def __init__(self):
    
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
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

    def get_field(self, x, y):
        content = []
        if x < 0 and y < 0 and x >= Board.sizeX or y >= Board.sizeY:
            logging.error("Field [%d, %d] out of bounds", x, y)
            return content
        
        else:
            if x == self.player.x and y == self.player.y:
                content.append('player')
            if x == self.enemy.x and y == self.enemy.y:
                content.append('enemy')
            
            for ladder_x, ladder_y in self.ladders:
                if x == ladder_x and y == ladder_y:
                    content.append('ladder')
                    break
                    
            for platform_x, platform_y in self.platforms:
                if x == platform_x and y == platform_y:
                    content.append('platform')
                    break                
            
        return content

    def free_fall(self, sprite):
        if sprite.y < Board.sizeY - 1 and not self.has_platform_below(sprite.x, sprite.y):
            sprite.y += 1
        
        logging.info('Sprite position (%d, %d)', sprite.x, sprite.y)
            
            
    def has_platform_below(self, x, y):
        logging.info('Field [%d, %d] contains %s', x, y, self.get_field(x, y))
        return 'platform' in self.get_field(x, y)
        