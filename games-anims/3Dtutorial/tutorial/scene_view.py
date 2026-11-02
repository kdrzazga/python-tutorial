from OpenGL.GL import *
from OpenGL.GLU import *


class FloorGrid:
    def __init__(self):
        self.half_extent = 3.0
        self.cell_size = 0.5
        self.height = -1.2
        self.color = (0.14, 0.16, 0.24)

    def draw(self):
        cell_count = int(2 * self.half_extent / self.cell_size)
        glLineWidth(1.0)
        glColor3f(*self.color)
        glBegin(GL_LINES)
        for cell_index in range(cell_count + 1):
            offset = -self.half_extent + cell_index * self.cell_size
            glVertex3f(offset, self.height, -self.half_extent)
            glVertex3f(offset, self.height, self.half_extent)
            glVertex3f(-self.half_extent, self.height, offset)
            glVertex3f(self.half_extent, self.height, offset)
        glEnd()


class SceneView:
    def __init__(self, left, bottom, width, height):
        self.viewport = (left, bottom, width, height)
        self.field_of_view = 45.0
        self.camera_distance = 5.5
        self.camera_tilt = 22.0
        self.tilt_follow_rate = 2.0
        self.spin_speed = 25.0
        self.spin_angle = 0.0
        self.floor_grid = FloorGrid()

    def update(self, seconds, target_tilt):
        self.spin_angle = (self.spin_angle + self.spin_speed * seconds) % 360.0
        follow = min(self.tilt_follow_rate * seconds, 1.0)
        self.camera_tilt += (target_tilt - self.camera_tilt) * follow

    def draw(self, lesson):
        width, height = self.viewport[2], self.viewport[3]
        glViewport(*self.viewport)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.field_of_view, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -self.camera_distance)
        glRotatef(self.camera_tilt, 1.0, 0.0, 0.0)
        glRotatef(self.spin_angle, 0.0, 1.0, 0.0)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        self.floor_grid.draw()
        lesson.draw()
        glDisable(GL_DEPTH_TEST)
