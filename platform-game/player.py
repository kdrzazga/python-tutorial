from enum import Enum

import arcade

from lib import Constants


class PlayerStatus(Enum):
    STANDING = 1
    RUNNING = 2
    FALLING = 3
    CLIMBING = 4


class PlatformPlayer(arcade.Sprite):
    def __init__(self):
        super().__init__("player.png", 1)
        self.change_x = 0
        self.change_y = 0
        self.center_x = 400
        self.center_y = 30
        self.status: PlayerStatus = PlayerStatus.STANDING

    def update(self):
        self.center_x += self.change_x
        self.change_y -= Constants.GRAVITY

        if self.center_y < 30:  # Bottom level
            self.center_y = 30
            self.change_y = 0
            self.jumping = False

        elif 300 > self.center_y >= 30:  # Middle level
            self.center_y = 300
            self.change_y = 0
            self.jumping = False

        elif self.center_y >= 300:  # Top level
            if self.center_x < 800 - Constants.PLAYER_SIZE // 2 and self.center_y >= 500:
                self.center_y = 500
                self.change_y = 0
                self.jumping = False

    def info(self):
        print(f"({self.change_y}, {self.center_y})")
