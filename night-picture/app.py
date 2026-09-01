import pygame
from OpenGL.GL import (
    GL_BLEND,
    GL_DEPTH_TEST,
    GL_LINE_SMOOTH,
    GL_MODELVIEW,
    GL_MULTISAMPLE,
    GL_POINT_SMOOTH,
    GL_PROJECTION,
    glDisable,
    glEnable,
    glLoadIdentity,
    glMatrixMode,
    glViewport,
)
from OpenGL.GLU import gluOrtho2D

from painter import Painter


class App:
    def __init__(self, scene, title="Night Picture"):
        self.scene = scene
        self.width = scene.width
        self.height = scene.height
        self.title = title

    def _configure_context(self):
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)

    def _configure_gl(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, self.width, 0.0, self.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_MULTISAMPLE)

    def run(self):
        pygame.init()
        self._configure_context()
        pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(self.title)
        self._configure_gl()

        painter = Painter(self.width, self.height)
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            time_seconds = pygame.time.get_ticks() / 1000.0
            self.scene.render(painter, time_seconds)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
