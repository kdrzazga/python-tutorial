import sys

import pygame
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective

from common import TextureLibrary
from nebula import Config, Scene
from round_nebula import RoundNebula


class NebulaApp:
    def __init__(self, config=None):
        self.config = config or Config()
        self.clock = None
        self.textures = None
        self.scene = None
        self.round_nebulas = ()
        self.time = 0.0
        self.running = False

    def _init_display(self):
        pygame.init()
        size = (self.config.width, self.config.height)
        flags = pygame.OPENGL | pygame.DOUBLEBUF
        try:
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
            pygame.display.set_mode(size, flags)
        except pygame.error:
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 0)
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 0)
            pygame.display.set_mode(size, flags)
        pygame.display.set_caption(self.config.title)

    def _init_gl(self):
        glClearColor(*self.config.background)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glDisable(GL_DEPTH_TEST)
        glDepthMask(GL_FALSE)
        glDisable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        self._resize(self.config.width, self.config.height)

    def _resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.config.fov, width / float(height), self.config.near, self.config.far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def _build_round_nebulas(self):
        glow = self.textures.glow
        return (
            RoundNebula(glow, center=(-530.0, 55.0, -95.0), radius=130.0, seed=3, spin_speed=10.1),
            RoundNebula(glow, center=(-630.0, -255.0, 155.0), radius=30.0, seed=2,  inner_color=(0.1, 0.96, 0.1)),
            RoundNebula(glow, center=(0.0, 0.0, 1500.0), radius=130.0, seed=2, spin_speed=0.1, rim_color=(0.0, 0.94, 0.30)),
            RoundNebula(glow, center=(-400.0, -400.0, 1600.0), radius=120.0, seed=5, spin_speed=-0.9, rim_color=(0.0, 0.15, 0.99)),
            RoundNebula(glow, center=(300.0, 450.0, 1650.0), radius=110.0, seed=1, spin_speed=-5.5),
            RoundNebula(glow, center=(255.0, -65.0, -150.0), radius=42.0, seed=6,
                        rim_color=(1.0, 0.34, 0.30), shell_color=(1.0, 0.58, 0.34),
                        inner_color=(0.40, 0.46, 0.92), spin_speed=-0.045),
        )

    def _events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def run(self):
        self._init_display()
        self._init_gl()
        self.textures = TextureLibrary()
        self.scene = Scene(self.config, self.textures)
        self.round_nebulas = self._build_round_nebulas()
        self.clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.time += self.clock.tick(self.config.fps) / 1000.0
            self._events()
            if self.time >= self.config.move_away_delay:
                self.scene.camera.move_away(1)
            self.scene.update(self.time)
            for nebula in self.round_nebulas:
                nebula.update(self.time)
            glClear(GL_COLOR_BUFFER_BIT)
            self.scene.render()
            for nebula in self.round_nebulas:
                nebula.render(self.scene.camera.right, self.scene.camera.up)
            pygame.display.flip()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    NebulaApp().run()
