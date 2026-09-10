import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT, KEYDOWN, K_ESCAPE
from OpenGL.GL import *
from OpenGL.GLU import *

from camera import Camera
from chessboard import Chessboard
from fog import Fog


class ChessboardFogAnimation:
    def __init__(self, window_size=(1024, 768), shade=(0.95, 0.05, 0.0), field_of_view=60.0):
        self.window_size = window_size
        self.shade = shade
        self.field_of_view = field_of_view
        self.camera = Camera(target=(0.0, 0.0, 0.0), orbit_radius=11.0, orbit_height=6.5,
                             orbit_speed_degrees=9.0, bob_amplitude=1.3, bob_speed=0.45)
        self.chessboard = Chessboard(squares_per_side=8, square_size=1.6, shade=shade)
        self.fog = Fog(shade=shade, particle_count=140, volume_radius=7.0, volume_bottom=0.3,
                       volume_top=4.5, start_distance=8.0, end_distance=30.0)
        self.clock = pygame.time.Clock()
        self.running = False

    def _setup_opengl(self):
        width, height = self.window_size
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.field_of_view, width / float(height), 0.1, 80.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        background = self.fog.background_color
        glClearColor(background[0], background[1], background[2], 1.0)
        self.fog.configure()

    def run(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
        pygame.display.set_mode(self.window_size, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Chessboard with Fog")
        self._setup_opengl()
        self.running = True
        start_ticks = pygame.time.get_ticks()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.running = False
            elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000.0
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.camera.apply(elapsed_seconds)
            camera_right, camera_up = self.camera.billboard_axes()
            self.chessboard.draw()
            self.fog.draw(elapsed_seconds, camera_right, camera_up)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    ChessboardFogAnimation().run()
