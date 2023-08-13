import logging

from enemy import Enemy
from player import Player

from fireball import Fireball
from factory import create_platforms, create_ladders


def decode_move(sprite, move):
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
        y2 = sprite.y + 1

    return x2, y2


class Board:
    sizeX = 17
    sizeY = 10

    def __init__(self):

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        self.player = Player(16, 6)
        self.enemies = [Enemy(0, 3), Enemy(4, 3), Enemy(3, 0), Enemy(7, 1), Enemy(8, 1), Enemy(9, 1), Enemy(10, 1),
                        Enemy(15, 0)]
        self.fireballs = [Fireball(0, 0), Fireball(0, 0)]

        self.platforms = create_platforms(Board.sizeX, Board.sizeY)
        self.ladders = create_ladders(Board.sizeY)

        self.status = 'running'

    def get_field(self, x, y):
        content = []
        if 0 > x >= Board.sizeX and y < 0 or y >= Board.sizeY:
            logging.error("Field [%d, %d] out of bounds", x, y)
            return content

        else:
            if x == self.player.x and y == self.player.y:
                content.append('player')
            if any(x == enemy.x and y == enemy.y for enemy in self.enemies):
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
        if not sprite.active:
            logging.debug("Sprite INACTIVE. Won't be moved")

        else:
            target_x, target_y = decode_move(sprite, direction)
            logging.debug('Moving sprite %s : (%d, %d) -> (%d, %d)', sprite.name, sprite.x, sprite.y, target_x,
                          target_y)
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
            logging.debug('Invalid move')
            return

        current_content = self.get_field(sprite.x, sprite.y)
        target_content = self.get_field(target_x, target_y)

        # ladder -> ladder
        if 'ladder' in current_content and 'ladder' in target_content:
            logging.debug('Ladders are present.Move sprite (%d, %d) -> (%d, %d)', sprite.x, sprite.y, target_x,
                          target_y)
            sprite.x, sprite.y = target_x, target_y

        # platform -> nothing (and free fall)
        # elif not any(['platform' in content for content in target_content]):
        #    logging.debug('Move sprite and check for free fall')
        #    if sprite.y < Board.sizeY - 1:
        #        sprite.y += 1
        else:  # platform -> platform
            sprite.x, sprite.y = target_x, target_y

    def move_fireballs(self):
        if self.fireballs[0].x > 0:
            self.fireballs[0].x -= 1
        if self.fireballs[1].x < Board.sizeX - 1:
            self.fireballs[1].x += 1

        if self.fireballs[0].x <= 0 and self.fireballs[1].x >= Board.sizeX - 1:
            return False

        return True

    def start_fireballs(self):
        self.fireballs[0].x = self.player.x - 1
        self.fireballs[0].y = self.player.y
        self.fireballs[1].x = self.player.x + 1
        self.fireballs[1].y = self.player.y
        self.player.spells -= 1

    def detect_player_collision(self, enemy):
        if enemy.x == self.player.x and enemy.y == self.player.y and self.player.active and enemy.active:
            self.player.energy -= 1
            if self.player.energy <= 0:
                self.player.active = False

    def detect_enemy_fb_collision(self, enemy):
        for fb in self.fireballs:
            if enemy.x == fb.x and enemy.y == fb.y:
                enemy.active = False
                logging.debug('Enemy hit at (%d, %d)', enemy.x, enemy.y)
                self.player.score += Enemy.score

    def free_fall(self, sprite):
        if sprite.y < Board.sizeY - 1 and not self.has_platform_below(sprite.x, sprite.y):
            sprite.y += 1

        logging.debug('Sprite "%s" position (%d, %d)', sprite.name, sprite.x, sprite.y)

    def has_platform_below(self, x, y):
        logging.debug('Field [%d, %d] contains %s', x, y, self.get_field(x, y))
        return 'platform' in self.get_field(x, y)
