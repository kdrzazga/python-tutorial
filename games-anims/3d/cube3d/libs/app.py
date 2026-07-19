import os
import time

import colorama
from colorama import Cursor
import pygame
from pygame.locals import DOUBLEBUF, FULLSCREEN, KEYDOWN, K_ESCAPE, K_SPACE, OPENGL, QUIT
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

from cube3d.amiga_dos_face import AmigaDOSFace
from cube3d.atari_face import AtariFace
from cube3d.c64_face import C64Face
from cube3d.oscilloscope_face import OscilloscopeFace
from cube3d.plasma_face import PlasmaFace
from cube3d.zx_spectrum_face import ZXSpectrumFace
from .caption import Caption
from .cube import Cube
from .amiga_ball import AmigaBall
from .globals import start_time, MUSIC_PATH, INFO_LINES1, INFO_LINES2
from .text_overlay import TextOverlay
from .tunnel_effect import TunnelEffect

TEX_SIZE = 256
WINDOW_SIZE = (900, 700)

CAPTION_Z = -16.0       # depth the scrolling caption sits at
CAPTION_SPEED = 3.0     # world units per second, right to left
CAPTION_MARGIN = 9.0    # extra travel so it fully leaves the screen before wrapping
BALL_Z = -8.0           # depth the Amiga ball sits at



class CubeApp:
    def __init__(self, windowed=False):
        self.windowed = windowed
        self.window_size = WINDOW_SIZE   # replaced by the real size in run()

        self.rotation_speed_x = 10
        self.rotation_speed_y = 18
        self.camera_y = 0.0
        self.camera_z = -6.0

        self.cube_offset = [0.0, 0.0, 0.0]
        self.second_cube_offset = [-3.0, 0.0, -5.0]  # left and back of the original

        text = ("Retro computers such as the Commodore, Atari, ZX Spectrum, and Amiga played a pivotal role in shaping"
                " home computing and gaming.   These machines are remembered for their innovative features and their influence"
                " on the development of digital entertainment")
        self.caption1 = Caption(text)
        # Start fully off-screen to the right, then scroll left and wrap.
        self.caption_span = self.caption1.world_width / 2 + CAPTION_MARGIN
        self.caption_x = self.caption_span

        self.tunnel = TunnelEffect()
        self.amiga_ball = AmigaBall(radius = 1.5)

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
        colorama.init()
        print(colorama.ansi.clear_screen(), end="")

        pygame.init()
        self.window_size, flags = self._display_mode()
        pygame.display.set_mode(self.window_size, flags)
        pygame.display.set_caption("Retro Screens on a CUBE")
        clock = pygame.time.Clock()

        if os.path.exists(MUSIC_PATH):
            pygame.mixer.music.load(MUSIC_PATH)
            pygame.mixer.music.play(loops=-1)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glClearColor(0.05, 0.05, 0.08, 1.0)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, self.window_size[0] / self.window_size[1], 0.1, 50.0)
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
        self.overlay = TextOverlay(self.window_size)
        self.caption1.prepare()   # pre-build now; avoids a freeze when the scroll starts

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
            glTranslatef(0.0, self.camera_y, self.camera_z)

            self.procedure(dt, t)

            pygame.display.flip()
            clock.tick(60)
            self._print_elapsed(t)

        pygame.quit()

    def procedure(self, dt, t):
        if t < 100:
            self._draw_cube(self.cube, self.angle_x, self.angle_y, self.cube_offset)
        if 33 < t:
            self._draw_cube(self.second_cube, self.second_angle_x, self.second_angle_y,
                            self.second_cube_offset)
        self.overlay.draw(t)
        if 20 < t < 22:
            self.camera_z -= 0.4
        elif 22 < t < 24:
            self.camera_z += 0.4
        elif 24 < t < 26:
            self.rotation_speed_y += 5
        elif 31 < t < 33:
            self.rotation_speed_y -= 5
        elif 50 < t:
            self.move_caption(dt)
        if 53 < t < 57:
            self.cube_offset[2] -= 0.08
        if 54 < t < 68:
            self.second_cube_offset[2] -= 0.08
        if 65 < t < 75:
            self.caption1.lean += 0.11
        if 75 < t < 95:
            self.caption1.lean -= 0.11
        if t > 80 and self.camera_y > -5:
            self.camera_y -= 0.01
        if t > 90:
            self.tunnel.render(dt)
        if 100 < t < 160:
            self.draw_amiga_ball(dt)
            if 110 < t < 130:
                self.amiga_ball.spin_speed += 0.5
            elif 130 < t < 150:
                self.amiga_ball.spin_speed -= 0.5
            if t> 130:
                self.amiga_ball.tilt += 1

    def draw_amiga_ball(self, dt):
        self.amiga_ball.update(dt)

        glPushMatrix()
        glLoadIdentity()          # ignore camera_y, which by now is far below the view
        glTranslatef(0.0, 0.0, BALL_Z)
        self.amiga_ball.render()
        glPopMatrix()

    def _display_mode(self):
        """Window size and pygame flags; fullscreen uses the desktop resolution."""
        if self.windowed:
            return WINDOW_SIZE, DOUBLEBUF | OPENGL

        desktop = pygame.display.Info()
        return (desktop.current_w, desktop.current_h), DOUBLEBUF | OPENGL | FULLSCREEN

    def _print_elapsed(self, t):
        for i, line in enumerate(INFO_LINES1):
            print(Cursor.POS(1, i+2) + line, flush=True)
        print(Cursor.POS(1, len(INFO_LINES1) + 2) + f"elapsed: {t:7.2f} s", end="", flush=True)

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

    def move_caption(self, dt):
        self.caption_x -= CAPTION_SPEED * dt
        if self.caption_x < -self.caption_span:
            self.caption_x = self.caption_span

        glPushMatrix()
        glLoadIdentity()
        glTranslatef(self.caption_x, self.camera_y, CAPTION_Z)
        self.caption1.render()
        glPopMatrix()
