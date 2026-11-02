from lesson1_pixel import Point
from lesson2_line import Line
from lesson3_triangle import Triangle, TriangleScene
from tutorial_window import Scene, TutorialWindow


class Trihedron:
    def __init__(self, base, apex):
        self.base = base
        self.apex = apex
        first, second, third = base.corners
        self.faces = (base,
                      Triangle(first, second, apex),
                      Triangle(second, third, apex),
                      Triangle(third, first, apex))
        self.edges = base.edges + (Line(first, apex),
                                   Line(second, apex),
                                   Line(third, apex))
        self.corners = base.corners + (apex,)

    def draw(self):
        for face in self.faces:
            face.draw_face()
        for edge in self.edges:
            edge.draw()
        for corner in self.corners:
            corner.draw()


class TrihedronScene(Scene):
    def __init__(self):
        base = TriangleScene().triangle
        apex = Point(0.0, 1.2, 0.1, (1.0, 0.9, 0.3))
        self.trihedron = Trihedron(base, apex)

    def draw(self):
        self.trihedron.draw()


if __name__ == "__main__":
    TutorialWindow("Lesson 4 - a trihedron").run(TrihedronScene())
