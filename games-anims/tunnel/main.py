import arcade
import random
import math

WIDTH = 800
HEIGHT = 600
NUM_DOTS = 400


class Dot:
    def __init__(self):
        self.reset()

    def reset(self):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(300, 600)
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


class TunnelWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Tunnel Effect")
        arcade.set_background_color(arcade.color.BLACK)
        self.dots = [Dot() for _ in range(NUM_DOTS)]

    def on_draw(self):
        self.clear()
        for dot in self.dots:
            arcade.draw_circle_filled(dot.x, dot.y, dot.size, arcade.color.WHITE)

    def on_update(self, delta_time):
        for dot in self.dots:
            dot.update()


if __name__ == "__main__":
    window = TunnelWindow()
    arcade.run()
