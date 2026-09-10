from OpenGL.GL import *


class Chessboard:
    def __init__(self, squares_per_side, square_size, shade):
        self.squares_per_side = squares_per_side
        self.square_size = square_size
        self.shade = shade
        self.dark_color = (0.0, 0.0, 0.0)
        self.light_color = shade if shade is not None else (1.0, 1.0, 1.0)

    def draw(self):
        half_span = self.squares_per_side * self.square_size / 2.0
        glBegin(GL_QUADS)
        for row in range(self.squares_per_side):
            for column in range(self.squares_per_side):
                if (row + column) % 2 == 0:
                    glColor3f(*self.light_color)
                else:
                    glColor3f(*self.dark_color)
                near_x = column * self.square_size - half_span
                near_z = row * self.square_size - half_span
                far_x = near_x + self.square_size
                far_z = near_z + self.square_size
                glVertex3f(near_x, 0.0, near_z)
                glVertex3f(far_x, 0.0, near_z)
                glVertex3f(far_x, 0.0, far_z)
                glVertex3f(near_x, 0.0, far_z)
        glEnd()
