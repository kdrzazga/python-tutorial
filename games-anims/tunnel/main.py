import arcade
import random
import math
from time import time

WIDTH = 800
HEIGHT = 600
NUM_DOTS = 400


class Dot:
    def __init__(self):
        self.speed = 0.0
        self.size = 1
        self.y = WIDTH / 2
        self.x = HEIGHT / 2
        self.reset()

    def reset(self):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(30, min(WIDTH, HEIGHT))
        self.x = WIDTH / 2 + math.cos(angle) * radius
        self.y = HEIGHT / 2 + math.sin(angle) * radius
        self.size = 1
        self.speed = 0.0

    def update(self):
        dx = (WIDTH / 2) - self.x
        dy = (HEIGHT / 2) - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance
        acceleration = 0.2
        self.speed += acceleration
        self.x += dx * self.speed
        self.y += dy * self.speed
        if distance < 10:
            self.reset()


class TunnelEffect:

    def __init__(self, enlarge_delay):
        self.dots = [Dot() for _ in range(NUM_DOTS)]
        self.dot_size = 1
        self.enlarge_time = time() + enlarge_delay

    def draw(self):
        for dot in self.dots:
            arcade.draw_circle_filled(dot.x, dot.y, self.dot_size, arcade.color.WHITE)

    def update(self):
        print(self.enlarge_time, time())
        if self.enlarge_time < time() and self.dot_size < 0.12*WIDTH:
            self.dot_size += 0.05 + 0.01*self.dot_size**1.2

        for dot in self.dots:
            dot.update()


class TunnelWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Tunnel Effect")
        arcade.set_background_color(arcade.color.BLACK)
        self.effect = TunnelEffect(8)

    def on_draw(self):
        self.clear()
        self.effect.draw()

    def on_update(self, delta_time):
        self.effect.update()


if __name__ == "__main__":
    window = TunnelWindow()
    arcade.run()
