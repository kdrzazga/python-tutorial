import time

import arcade

from src.main.images_helper import HondaMovesRegistry, MovesRegistry
from src.main.project_globals import Constants


class Fighter:
    def __init__(self, arena_offset):
        self.walk_phase = arcade.load_texture("resources/honda_stand.png")
        self.x = Constants.SCREEN_WIDTH + 350
        self.y = 220
        self.state = "idle"
        self.speed = 3
        self.punch_duration = 0.5
        self.punch_start_time = 0
        self.arena_offset = arena_offset

        self.stand_image = None
        self.punch_image = None

        self.step_delay_counter = 0
        self.moves_registry = MovesRegistry()

        self.punch_sound = arcade.load_sound("resources/uaja.mp3")

    def start_punch(self):
        if self.state == "idle":
            self.state = "punching"
            self.shout()
            self.punch_start_time = time.time()

    def move_right(self):

        self.state = "walking"
        self.x -= self.speed
        self.step_anim()

    def move_left(self):

        self.state = "walking"
        self.x += self.speed
        self.step_anim()

    def step_anim(self):
        self.step_delay_counter += 1
        if self.step_delay_counter % 10 == 0:
            self.walk_phase = self.moves_registry.next()

        if self.step_delay_counter > 300:
            self.step_delay_counter = 0

    def shout(self):
        arcade.play_sound(self.punch_sound)

    def update(self):
        if self.state == "punching" and (time.time() - self.punch_start_time > self.punch_duration):
            self.state = "idle"

    def draw(self):
        x = Constants.SCREEN_WIDTH - self.x // 2
        y = Constants.SCREEN_HEIGHT - self.y - self.arena_offset // 2
        if self.state == "punching":
            arcade.draw_texture_rectangle(x, y - self.punch_image.width // 2,
                                          self.punch_image.width, self.punch_image.height, self.punch_image)
        elif self.state == "walking":
            arcade.draw_texture_rectangle(x, y - self.stand_image.width // 2,
                                          self.stand_image.width, self.stand_image.height, self.walk_phase)
        else:
            arcade.draw_texture_rectangle(x, y - self.stand_image.width // 2,
                                          self.stand_image.width, self.stand_image.height, self.stand_image)


class Honda(Fighter):
    def __init__(self, arena_offset):
        super().__init__(arena_offset)
        self.stand_image = arcade.load_texture("resources/honda_stand.png")
        self.punch_image = arcade.load_texture("resources/honda_punch.png")

        self.moves_registry = HondaMovesRegistry()

