import math
import random

import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_CIRCLES = 50
TUNNEL_DEPTH = 300
SPEED = 2

class Circle:
    def __init__(self, center_x, y, radius, color):
        self.center_x = center_x
        self.y = y
        self.radius = radius
        self.color = color
        self.z = 0  # depth for perspective effect

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.y, self.radius, self.color)

    def update(self):
        if self.radius < 0.98*max(SCREEN_WIDTH, SCREEN_HEIGHT):
            self.radius += 2+self.radius/48
        if self.radius >= 0.98 * max(SCREEN_WIDTH, SCREEN_HEIGHT):
            self.radius = 1


class CircleTunnel:
    def __init__(self):
        self.timer = 0
        self.circles = []
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2

        for i in range(NUM_CIRCLES):
            radius = 44 * i
            color = (
                random.randint(170, 255),
                random.randint(0, 75),
                random.randint(0, 75),
            )
            self.circles.append(Circle(self.center_x, self.center_y, radius, color))

    def draw(self):
        for circle in self.circles:
            arcade.draw_circle_outline(circle.center_x, circle.y, circle.radius, circle.color)

    def update(self):
        self.timer += 1
        modifier = 3*self.find_modifier()

        for circle in self.circles:
            circle.update()
            if circle.radius < 150:
                circle.center_x += modifier

    def find_modifier(self):
        cycle_time = (self.timer // 14) % 3
        if cycle_time == 0:
            modifier = 1
        elif cycle_time == 1:
            modifier = -1
        else:  # cycle_time == 2
            modifier = 0
        return modifier


class TunnelWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Circle Tunnel Effect")
        self.tunnel = CircleTunnel()

    def on_draw(self):
        self.clear()
        self.tunnel.draw()

    def on_update(self, delta_time):
        self.tunnel.update()


def main():
    window = TunnelWindow()
    arcade.run()


if __name__ == "__main__":
    main()
