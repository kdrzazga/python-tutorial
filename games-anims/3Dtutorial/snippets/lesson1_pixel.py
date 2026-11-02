import colorsys

from OpenGL.GL import *

from tutorial_window import Scene, TutorialWindow


class Point:
    def __init__(self, x, y, z, color=(1.0, 1.0, 1.0)):
        self.position = (x, y, z)
        self.color = color
        self.size = 12.0

    def change_color(self, red, green, blue):
        self.color = (red, green, blue)

    def draw(self):
        glPointSize(self.size)
        glBegin(GL_POINTS)
        glColor3f(*self.color)
        glVertex3f(*self.position)
        glEnd()


class PixelScene(Scene):
    def __init__(self):
        self.pixel = Point(0.0, 0.0, 0.0)
        self.hue = 0.0
        self.hue_speed = 0.25

    def update(self, seconds):
        self.hue = (self.hue + self.hue_speed * seconds) % 1.0
        red, green, blue = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        self.pixel.change_color(red, green, blue)

    def draw(self):
        self.pixel.draw()


if __name__ == "__main__":
    TutorialWindow("Lesson 1 - a pixel").run(PixelScene())
