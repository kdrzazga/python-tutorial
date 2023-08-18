import logging

from bartender import Player


class Board:

    def __init__(self):
        self.player = Player()
        self.player_slot = 0
        self.slots = [None] * 4

    def move_player_up(self):
        logging.debug('moving UP')
        self.player_slot = (self.player_slot - 1) % len(self.slots)
        logging.debug('Theb bantender is at slot ' + str(self.player_slot))

    def move_player_down(self):
        logging.debug('moving DOWN')
        self.player_slot = (self.player_slot + 1) % len(self.slots)
        logging.debug('Theb bantender is at slot ' + str(self.player_slot))

    def move_player_left(self):
        logging.debug('moving LEFT')
        self.player.set_status('bar')
        logging.debug('status ' + self.player.status)

    def move_player_right(self):
        logging.debug('moving RIGHT')
        self.player.set_status('counter')
        logging.debug('status ' + self.player.status)
