import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


class Scene:
    def update(self, seconds):
        pass

    def draw(self):
        raise NotImplementedError


class TutorialWindow:
    def __init__(self, title):
        self.width = 800
        self.height = 600
        self.background_color = (0.04, 0.05, 0.09, 1.0)
        self.camera_distance = 5.5
        self.camera_tilt = 22.0
        self.spin_speed = 25.0
        self.spin_angle = 0.0
        pygame.init()
        pygame.display.set_caption(title)
        pygame.display.set_mode((self.width, self.height),
                                pygame.DOUBLEBUF | pygame.OPENGL)
        self.clock = pygame.time.Clock()

    def setup_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, self.width / self.height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

    def is_closing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
        return False

    def run(self, scene):
        self.setup_camera()
        while not self.is_closing():
            seconds = self.clock.tick(60) / 1000.0
            self.spin_angle = (self.spin_angle + self.spin_speed * seconds) % 360.0
            scene.update(seconds)
            glClearColor(*self.background_color)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0.0, 0.0, -self.camera_distance)
            glRotatef(self.camera_tilt, 1.0, 0.0, 0.0)
            glRotatef(self.spin_angle, 0.0, 1.0, 0.0)
            scene.draw()
            pygame.display.flip()
        pygame.quit()
