import os
import time

import pygame
from pygame.locals import DOUBLEBUF, KEYDOWN, K_ESCAPE, K_SPACE, OPENGL, QUIT
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_TEXTURE_2D,
    glClear,
    glClearColor,
    glEnable,
    glLoadIdentity,
    glMatrixMode,
    glRotatef,
    glTranslatef,
    GL_MODELVIEW,
    GL_PROJECTION,
)
from OpenGL.GLU import gluPerspective

from .amiga_dos_face import AmigaDOSFace
from .atari_face import AtariFace
from .c64_face import C64Face
from .cube import Cube
from .oscilloscope_face import OscilloscopeFace
from .globals import MUSIC_PATH
from .plasma_face import PlasmaFace
from .zx_spectrum_face import ZXSpectrumFace

TEX_SIZE = 256
WINDOW_SIZE = (900, 700)


class CubeApp:
    def __init__(self):
        self.generators = None
        self.cube = None
        self.angle_x, self.angle_y = 20.0, 30.0
        self.auto_rotate = True
        self.dragging = False
        self.last_mouse = (0, 0)

    def run(self):
        pygame.init()
        pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Live 3D Cube - Commodore 64 Edition")
        clock = pygame.time.Clock()

        if os.path.exists(MUSIC_PATH):
            pygame.mixer.music.load(MUSIC_PATH)
            pygame.mixer.music.play(loops=-1)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glClearColor(0.05, 0.05, 0.08, 1.0)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, WINDOW_SIZE[0] / WINDOW_SIZE[1], 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

        # Face generators load fonts, so they must be built after pygame.init().
        self.generators = [
            PlasmaFace(TEX_SIZE),
            AmigaDOSFace(TEX_SIZE),
            AtariFace(TEX_SIZE),
            ZXSpectrumFace(TEX_SIZE),
            C64Face(TEX_SIZE),
            OscilloscopeFace(TEX_SIZE),
        ]
        self.cube = Cube(TEX_SIZE)

        start_time = time.time()
        prev_time = start_time

        running = True
        while running:
            now = time.time()
            t = now - start_time
            dt = now - prev_time
            prev_time = now

            running = self._handle_events(dt)

            surfaces = [gen.render(t) for gen in self.generators]
            self.cube.upload(surfaces)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0.0, 0.0, -6.0)
            glRotatef(self.angle_x, 1, 0, 0)
            glRotatef(self.angle_y, 0, 1, 0)

            self.cube.draw()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def _handle_events(self, dt):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_SPACE:
                    self.auto_rotate = not self.auto_rotate
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.dragging = True
                self.last_mouse = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                dx = event.pos[0] - self.last_mouse[0]
                dy = event.pos[1] - self.last_mouse[1]
                self.angle_y += dx * 0.4
                self.angle_x += dy * 0.4
                self.last_mouse = event.pos

        if self.auto_rotate and not self.dragging:
            self.angle_y += 18 * dt
            self.angle_x += 9 * dt

        return True
