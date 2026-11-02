import math

from lesson8_mesh import MeshSurface
from tutorial_window import Scene, TutorialWindow


class Wave:
    def __init__(self, amplitude, length, heading_degrees, speed):
        heading = math.radians(heading_degrees)
        self.amplitude = amplitude
        self.wave_number = 2.0 * math.pi / length
        self.direction = (math.cos(heading), math.sin(heading))
        self.speed = speed

    def height(self, x, z, time):
        direction_x, direction_z = self.direction
        distance = x * direction_x + z * direction_z
        travelled = distance - self.speed * time
        wave_angle = self.wave_number * travelled
        return self.amplitude * math.sin(wave_angle)


class SeaSurface(MeshSurface):
    def __init__(self, size, divisions):
        super().__init__(size, divisions)
        self.time = 0.0
        self.foam_height = 0.2
        self.foam_color = (0.9, 0.95, 1.0)
        self.foam_alpha = 0.6
        self.lines_duration = 4.0
        self.waves = (Wave(0.12, 2.2, 20.0, 0.9),
                      Wave(0.06, 1.1, -35.0, 0.7),
                      Wave(0.03, 0.6, 80.0, 0.5))

    def update(self, seconds):
        self.time += seconds

    def height(self, x, z):
        swell = sum(wave.height(x, z, self.time)
                    for wave in self.waves)
        return self.base_height + swell

    def foam_at(self, position):
        rise = (position[1] - self.base_height) / self.foam_height
        shade = min(max((rise + 1.0) / 2.0, 0.0), 1.0)
        return shade * shade

    def line_color_at(self, position):
        foam = self.foam_at(position)
        return tuple(channel + (1.0 - channel) * foam
                     for channel in self.line_color)

    def fill_color_at(self, position):
        foam = self.foam_at(position)
        red, green, blue = (water + (crest - water) * foam
                            for water, crest
                            in zip(self.fill_color, self.foam_color))
        alpha = self.fill_alpha
        alpha += (self.foam_alpha - alpha) * foam
        return (red, green, blue, alpha)

    def draw(self):
        positions = self.grid_positions()
        if self.time < self.lines_duration:
            every_line = range(self.divisions + 1)
            self.draw_rows(positions, every_line)
            self.draw_columns(positions, every_line)
        self.draw_fill(positions)


class SeaScene(Scene):
    def __init__(self):
        self.sea = SeaSurface(4.0, 24)

    def update(self, seconds):
        self.sea.update(seconds)

    def draw(self):
        self.sea.draw()


if __name__ == "__main__":
    TutorialWindow("Lesson 9 - sea waves").run(SeaScene())
