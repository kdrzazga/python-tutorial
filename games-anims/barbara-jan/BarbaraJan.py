import math

import arcade

from src.main.board import Board
from src.main.data import Data
from src.main.fighter import Honda, Karateka
from src.main.project_globals import Constants

KEYS = {
    "HONDA_RIGHT": arcade.key.D,
    "HONDA_LEFT": arcade.key.A,
    "KARATEKA_RIGHT": arcade.key.L,
    "KARATEKA_LEFT": arcade.key.J,
    "HONDA_PUNCH": [arcade.key.SPACE, arcade.key.LCTRL, arcade.key.LSHIFT],
    "KARATEKA_PUNCH": [arcade.key.ENTER, arcade.key.RCTRL, arcade.key.RSHIFT],
    "CHANGE_COLOR": arcade.key.F2,
    "QUIT": arcade.key.ESCAPE
}


class BarbaraJan(arcade.Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, "Barbara & Ian")
        self.set_fullscreen(True)
        self.board = Board()
        self.honda_fighter = Honda(self.board.arena_offset)
        self.karateka_fighter = Karateka(self.board.arena_offset)
        self.captions = "normal"
        self.random_draw_reset = True
        self.time = 0
        self.key_state = {key: False for key in (
            KEYS["HONDA_RIGHT"],
            KEYS["HONDA_LEFT"],
            KEYS["KARATEKA_RIGHT"],
            KEYS["KARATEKA_LEFT"],
            KEYS["CHANGE_COLOR"],
            KEYS["QUIT"],
        )}
        for key in KEYS["HONDA_PUNCH"]:
            self.key_state[key] = False
        for key in KEYS["KARATEKA_PUNCH"]:
            self.key_state[key] = False

    def on_draw(self):
        arcade.start_render()
        self.board.draw()
        self.karateka_fighter.draw()
        self.honda_fighter.draw()

    def update(self, delta_time):
        self.time += delta_time
        # print(self.time, end='\t')
        self.handle_dialogue()
        self.honda_fighter.update()
        self.karateka_fighter.update()
        self.handle_movement()

    def handle_dialogue(self):

        self.board.dialog = False

        if self.time < 3:
            self.board.dialog = True
            self.board.message_ptr = Data.fight_call

        t1 = math.floor(self.time) % 88

        if 15 < t1 < 24:
            self.board.dialog = True
            self.board.message_ptr = Data.honda_insult

        t2 = math.floor(self.time) % 51

        if 33 < t2 < 44:
            self.board.dialog = True
            if self.random_draw_reset:
                self.board.message_ptr = Data.get_random()
            self.random_draw_reset = False
        else:
            self.random_draw_reset = True

    def handle_movement(self):
        if self.key_state[KEYS["HONDA_RIGHT"]]:
            self.honda_fighter.move_right()

        if self.key_state[KEYS["HONDA_LEFT"]]:
            self.honda_fighter.move_left()

        if self.key_state[KEYS["KARATEKA_RIGHT"]]:
            self.karateka_fighter.move_right()

        if self.key_state[KEYS["KARATEKA_LEFT"]]:
            self.karateka_fighter.move_left()

        self.board.apply_boundaries(self.honda_fighter)
        self.board.apply_boundaries(self.karateka_fighter)

    def on_key_press(self, key, modifiers):
        if key in KEYS["HONDA_PUNCH"]:
            self.honda_fighter.start_punch()
        if key == KEYS["CHANGE_COLOR"]:
            print("Change karateka color.")
            self.karateka_fighter.change_color()
        if key in self.key_state.keys():
            self.key_state[key] = True
        if key in KEYS["KARATEKA_PUNCH"]:
            self.karateka_fighter.start_punch()
        if key == KEYS["QUIT"]:
            print("Bye !")
            arcade.exit()

    def on_key_release(self, key, modifiers):
        if key in (KEYS["HONDA_LEFT"], KEYS["HONDA_RIGHT"]):
            self.honda_fighter.state = "idle"
        elif key in (KEYS["KARATEKA_LEFT"], KEYS["KARATEKA_RIGHT"]):
            self.karateka_fighter.state = "idle"

        if key in self.key_state:
            self.key_state[key] = False
