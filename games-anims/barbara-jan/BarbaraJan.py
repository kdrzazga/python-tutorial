import math

import arcade

from src.main.board import Board
from src.main.data import Data
from src.main.fighter import Fighter, Honda, Karateka
from src.main.helper import check_distance, GameState
from src.main.intro import Intro
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
        self.set_fullscreen(False)
        self.game_on: GameState = GameState.INTRO

        self.intro = Intro()

        self.board = Board()
        self.honda_fighter = Honda(self.board.arena_offset)
        self.karateka_fighter = Karateka(self.board.arena_offset)
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
        if GameState.INTRO == self.game_on:
            self.intro.show()
        else:
            self.board.draw()
            self.draw_hp(self.honda_fighter)
            self.draw_hp(self.karateka_fighter)
            self.karateka_fighter.draw()
            self.honda_fighter.draw()

    def draw_hp(self, fighter: Fighter):
        radius = 13

        shift = Constants.SCREEN_WIDTH - 160 if isinstance(fighter, Karateka) else 26

        for i in range(fighter.hp):
            row = i // 3
            col = i % 3

            center_x = shift + col * (radius * 2 + 38)
            center_y = Constants.SCREEN_HEIGHT - row * (radius * 2 + 21) - 22
            arcade.draw_circle_filled(center_x, center_y, radius, Constants.RED)

    def update(self, delta_time):
        self.time += delta_time
        if self.time > 13 and self.game_on == GameState.INTRO:
            self.game_on = GameState.FIGHT
        # print(self.time, end='\t')

        if self.game_on != GameState.INTRO:
            self.handle_dialogue()
            self.honda_fighter.update()
            self.karateka_fighter.update()

        if self.game_on == GameState.FIGHT:
            self.handle_movement()

    def handle_dialogue(self):

        self.board.dialog = False

        if self.game_on == GameState.FIGHT:
            if self.time < 15:
                self.board.dialog = True
                self.board.message_ptr = Data.fight_call

            t1 = math.floor(self.time) % 97

            if 19 < t1 < 28:
                self.board.dialog = True
                self.board.message_ptr = Data.honda_insult

            t2 = math.floor(self.time) % 35

            if 30 < t2 < 33:
                self.board.dialog = True
                if self.random_draw_reset:
                    self.board.message_ptr = Data.get_random()
                self.random_draw_reset = False
            else:
                self.random_draw_reset = True

        elif self.game_on == GameState.KO_HONDA or self.game_on == GameState.KO_KARATEKA:
            self.board.dialog = True
            self.board.message_ptr = Data.fight_over

            print(f'Time = {self.time}')
            if math.floor(self.time) % 11 == 0:
                self.board.game_on = GameState.END
        else:
            self.board.dialog = True
            self.board.message_ptr = Data.reward


    def handle_movement(self):

        if self.honda_fighter.state == "dead" or self.karateka_fighter.state == "dead":
            return

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
        if key in self.key_state.keys():
            self.key_state[key] = True

        if key == KEYS["QUIT"]:
            print("Bye !")
            arcade.exit()

        if key == KEYS["CHANGE_COLOR"]:
            print("Change karateka color.")
            self.karateka_fighter.change_color()

        if self.game_on == GameState.FIGHT:

            if key in KEYS["HONDA_PUNCH"]:
                if self.honda_fighter.state != "dead":
                    self.honda_fighter.start_punch()

                    if check_distance(self.karateka_fighter.x, self.honda_fighter.x,
                                      self.karateka_fighter.stand_image.width, self.honda_fighter.stand_image.width):
                        self.game_on = self.karateka_fighter.receive_hit()

            if key in KEYS["KARATEKA_PUNCH"]:
                if self.karateka_fighter.state != "dead":
                    self.karateka_fighter.start_punch()
                    if check_distance(self.karateka_fighter.x, self.honda_fighter.x,
                                      self.karateka_fighter.stand_image.width, self.honda_fighter.stand_image.width):
                        self.game_on = self.honda_fighter.receive_hit()

    def on_key_release(self, key, modifiers):
        if self.honda_fighter.state == "dead" or self.karateka_fighter.state == "dead":
            return

        if key in (KEYS["HONDA_LEFT"], KEYS["HONDA_RIGHT"]):
            self.honda_fighter.state = "idle"
        elif key in (KEYS["KARATEKA_LEFT"], KEYS["KARATEKA_RIGHT"]):
            self.karateka_fighter.state = "idle"

        if key in self.key_state:
            self.key_state[key] = False
