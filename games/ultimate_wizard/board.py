import logging

from enemy import Enemy
from player import Player

from factory import create_platforms, create_ladders

class Board:

    sizeX = 17
    sizeY = 10

    def __init__(self):
    
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
        self.player = Player(16, 9)
        self.enemy = Enemy(9, 3)
    
        self.platforms = create_platforms(Board.sizeX)
        self.ladders = create_ladders(Board.sizeY)

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

    def move_sprite(self, sprite, direction):
        target_x, target_y = self.decode_move(sprite, direction)
        self._perform_sprite_move(sprite, target_x, target_y)

    def _perform_sprite_move(self, sprite, target_x, target_y):
        if (
            abs(target_x - sprite.x) > 1
            or abs(target_y - sprite.y) > 1
            or target_x < 0
            or target_x >= Board.sizeX
            or target_y < 0
            or target_y >= Board.sizeY
        ):
            return  # Invalid move, do nothing

        current_content = self.get_field(sprite.x, sprite.y)
        target_content = self.get_field(target_x, target_y)

        if 'ladder' in current_content and 'ladder' in target_content:
            sprite.x, sprite.y = target_x, target_y  # Move sprite up or down if ladders are present

        elif not any(['platform' in content for content in target_content]):
            self.free_fall(sprite)  # Move sprite and check for free fall

    def free_fall(self, sprite):
        if sprite.y < Board.sizeY - 1 and not self.has_platform_below(sprite.x, sprite.y):
            sprite.y += 1
        
        logging.info('Sprite position (%d, %d)', sprite.x, sprite.y)
     
    def has_platform_below(self, x, y):
        logging.info('Field [%d, %d] contains %s', x, y, self.get_field(x, y))
        return 'platform' in self.get_field(x, y)
        
    def decode_move(self, sprite, move):
        if move == 'l':
            x2 = sprite.x - 1
            y2 = sprite.y
        elif move == 'r':
            x2 = sprite.x + 1
            y2 = sprite.y
        elif move == 'u':
            x2 = sprite.x
            y2 = sprite.y - 1
        elif move == 'd':
            x2 = sprite.x
            y2 = sprite.y + 2
        
        return x2, y2
        