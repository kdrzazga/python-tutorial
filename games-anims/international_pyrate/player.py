import logging


class Player:
    directions = 'none', 'left', 'top left', 'right', 'top right'
    direction_file_dict = {'none': 'sprite.png', 'left': 'spriteML.png', 'top left': 'spriteTL.png',
                           'right': 'spriteMR.png', 'top right': 'spriteTR.png', }

    def __init__(self):
        self.score = 0
        self.sprite_path = "resources/sprite.png"
        self.direction = 'none'

    def set_direction(self, new_dir):
        self.direction = new_dir
        logging.debug("Direction: " + new_dir)
        self.sprite_path = "resources/" + Player.direction_file_dict[new_dir]
