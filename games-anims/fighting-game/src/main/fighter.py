import arcade
import time

class Fighter:
    def __init__(self):
        self.x = 200
        self.y = 220
        self.state = "idle"
        self.punch_duration = 0.5
        self.punch_start_time = 0

    def start_punch(self):
        if self.state == "idle":
            self.state = "punching"
            self.punch_start_time = time.time()

    def update(self):
        if self.state == "punching" and (time.time() - self.punch_start_time > self.punch_duration):
            self.state = "idle"

    def draw(self):
        if self.state == "punching":
            arcade.draw_texture_rectangle(self.x, self.y, 50, 100, arcade.color.RED)
        else:
            arcade.draw_texture_rectangle(self.x, self.y, 50, 50, arcade.color.BLUE)
