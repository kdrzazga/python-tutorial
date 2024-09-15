import arcade
import time

from src.main.constants import Constants

class Fighter:
    def __init__(self, arena_offset):
        self.x = Constants.SCREEN_WIDTH + 350
        self.y = 220
        self.state = "idle"
        self.punch_duration = 0.5
        self.punch_start_time = 0
        self.stand_image = None
        self.punch_image = None
        self.arena_offset = arena_offset

    def start_punch(self):
        if self.state == "idle":
            self.state = "punching"
            self.punch_start_time = time.time()

    def update(self):
        if self.state == "punching" and (time.time() - self.punch_start_time > self.punch_duration):
            self.state = "idle"

    def draw(self):
        if self.state == "punching":
            arcade.draw_texture_rectangle(Constants.SCREEN_WIDTH  - self.x //2,  Constants.SCREEN_HEIGHT - self.y - self.arena_offset //2 - self.punch_image.width // 2, self.punch_image.width, self.punch_image.height, self.punch_image)
        else:
            arcade.draw_texture_rectangle(Constants.SCREEN_WIDTH  - self.x //2,  Constants.SCREEN_HEIGHT - self.y - self.arena_offset // 2 - self.stand_image.width // 2, self.stand_image.width, self.stand_image.height, self.stand_image)


class Honda(Fighter):
    def __init__(self, arena_offset):
        super().__init__(arena_offset)
        self.stand_image = arcade.load_texture("resources/honda_stand.png")
        self.punch_image = arcade.load_texture("resources/honda_punch.png")
