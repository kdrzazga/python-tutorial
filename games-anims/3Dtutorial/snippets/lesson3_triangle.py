from OpenGL.GL import *

from lesson1_pixel import Point
from lesson2_line import Line, LineScene
from tutorial_window import Scene, TutorialWindow


class Triangle:
    def __init__(self, first, second, third):
        self.corners = (first, second, third)
        self.edges = (Line(first, second),
                      Line(second, third),
                      Line(third, first))
        self.fill_alpha = 0.35

    def draw_face(self):
        glEnable(GL_BLEND) # turns on blending. With it on,
        # OpenGL doesn’t overwrite the pixel already on screen.
        # It mixes the new colour with what’s there
        # so the triangle’s face can be see-through
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)
        glBegin(GL_TRIANGLES)
        for corner in self.corners:
            glColor4f(*corner.color, self.fill_alpha)
            glVertex3f(*corner.position)
        glEnd()
        glDepthMask(GL_TRUE)
        glDisable(GL_BLEND)

    def draw(self):
        self.draw_face()
        for edge in self.edges:
            edge.draw()
        for corner in self.corners:
            corner.draw()


class TriangleScene(Scene):
    def __init__(self):
        line_scene = LineScene()
        point_c = Point(0.1, -0.7, -1.2, (0.3, 0.5, 1.0))
        self.triangle = Triangle(line_scene.point_a,
                                 line_scene.point_b,
                                 point_c)

    def draw(self):
        self.triangle.draw()


if __name__ == "__main__":
    TutorialWindow("Lesson 3 - a triangle").run(TriangleScene())
