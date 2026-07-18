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
    glPopMatrix,
    glPushMatrix,
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
from .globals import start_time, MUSIC_PATH
from .plasma_face import PlasmaFace
from .text_overlay import TextOverlay
from .zx_spectrum_face import ZXSpectrumFace

TEX_SIZE = 256
WINDOW_SIZE = (900, 700)


class CubeApp:
    def __init__(self):
        self.rotation_speed_x = 10
        self.rotation_speed_y = 18
        self.camera_z = -6.0

        self.second_cube_offset = (-3.0, 0.0, -5.0)  # left and back of the original

        self.generators = None
        self.cube = None
        self.second_cube = None
        self.overlay = None
        self.angle_x, self.angle_y = 20.0, 30.0
        self.second_angle_x, self.second_angle_y = 20.0, 30.0
        self.auto_rotate = True
        self.dragging = False
        self.last_mouse = (0, 0)

    def run(self):
        pygame.init()
        pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Retro Screens on a CUBE")
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
        self.second_cube = Cube(TEX_SIZE)
        self.overlay = TextOverlay(WINDOW_SIZE)

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
            if 33 < t:
                self.second_cube.upload(surfaces)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0.0, 0.0, self.camera_z)

            self._draw_cube(self.cube, self.angle_x, self.angle_y)
            if 33 < t:
                self._draw_cube(self.second_cube, self.second_angle_x, self.second_angle_y,
                                self.second_cube_offset)

            self.overlay.draw(t)

            pygame.display.flip()
            clock.tick(60)

            print(t)

            if 20 < t < 22:
                self.camera_z -= 0.4
            elif 22 < t < 24:
                self.camera_z += 0.4
            elif 24 < t < 26:
                self.rotation_speed_y += 5
            elif 31 < t < 33:
                self.rotation_speed_y -= 5

        pygame.quit()

    def _draw_cube(self, cube, angle_x, angle_y, offset=(0.0, 0.0, 0.0)):
        glPushMatrix()
        glTranslatef(*offset)
        glRotatef(angle_x, 1, 0, 0)
        glRotatef(angle_y, 0, 1, 0)
        cube.draw()
        glPopMatrix()

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
            self.angle_y += self.rotation_speed_y * dt
            self.angle_x += self.rotation_speed_x * dt

        # The second cube rotates on its own, unaffected by mouse or keyboard.
        self.second_angle_y += self.rotation_speed_y * dt
        self.second_angle_x += self.rotation_speed_x * dt

        return True
