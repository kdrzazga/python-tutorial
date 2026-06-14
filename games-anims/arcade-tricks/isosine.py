import arcade
import math


class IsometricSineTunnel:
    def __init__(self, color: arcade.color.Color, angle_deg=66):
        self.angle_deg = angle_deg
        self.phase = 0
        self.color = color

    def update(self, delta_time, speed=2):
        self.phase += speed * delta_time

    def draw(self, surface_width, surface_height, amplitude, frequency, horizon_x):
        points = []
        angle_rad = math.radians(self.angle_deg)

        for y in range(0, surface_height, 2):
            sine_value = amplitude * math.sin(frequency * (y + self.phase))
            # Convert to isometric projection with x as the sine value
            iso_x, iso_y = self.iso_transform(sine_value + horizon_x, y, angle_rad, surface_width, surface_height)
            points.append((iso_x, iso_y))

        arcade.draw_lines(points, self.color, 1)

    def iso_transform(self, x, y, angle_rad, surface_width, surface_height):
        iso_x = x - y * math.cos(angle_rad)
        iso_y = y * math.sin(angle_rad)

        iso_x += surface_width / 4
        iso_y += surface_height / 4
        return iso_x, iso_y

# Main game window