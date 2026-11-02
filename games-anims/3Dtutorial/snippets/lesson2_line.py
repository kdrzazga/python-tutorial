from OpenGL.GL import *

from lesson1_pixel import Point
from tutorial_window import Scene, TutorialWindow


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.width = 3.0

    def draw(self):
        glLineWidth(self.width)
        glBegin(GL_LINES)
        glColor3f(*self.start.color)
        glVertex3f(*self.start.position)
        glColor3f(*self.end.color)
        glVertex3f(*self.end.position)
        glEnd()


class LineScene(Scene):
    def __init__(self):
        self.point_a = Point(-1.3, -0.8, 0.7, (1.0, 0.3, 0.3))
        self.point_b = Point(1.2, -0.4, 0.9, (0.3, 1.0, 0.4))
        self.line = Line(self.point_a, self.point_b)

    def draw(self):
        self.line.draw()
        self.point_a.draw()
        self.point_b.draw()


if __name__ == "__main__":
    TutorialWindow("Lesson 2 - a 3D line").run(LineScene())
