import os
import random
import time

import colorama
from colorama import Cursor, Fore, Style
import numpy as np
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
from .atari_logo import AtariLogo
from .zx_logo import ZxLogo
from .c64logo import C64Logo
from .glitch_overlay import GlitchOverlay
from .globals import start_time, ASSETS_DIR, MUSIC_PATH, INFO_LINES1, INFO_LINES2
from .screen_image import ScreenImage
from .text_overlay import TextOverlay
from .tunnel_effect import TunnelEffect

TEX_SIZE = 256
WINDOW_SIZE = (900, 700)

CAPTION_Z = -16.0       # depth the scrolling caption sits at
CAPTION_MARGIN = 9.0    # extra travel so it fully leaves the screen before wrapping
CAPTION_START = 50.0    # when the scroll begins
MUSIC_DURATION = 205.0  # fallback only; the real track length is measured at startup
CREDITS_DURATION = 2.0  # credits shown over the final seconds
EXIT_DELAY = 2.0        # quit this long after the music ends
SILENCE_LEVEL = 0.02    # share of peak below which the track counts as silent
BLINK_DURATION = 0.5    # how long a blinked picture stays on screen
BLINK_INTERFERENCE = 0.25   # share of scanlines dropped when the signal breaks up
GLITCH_CHANCE = 0.25        # share of frames that break up; the rest show it clean
BALL_Z = -8.0           # depth the Amiga ball sits at

SCENE_INTERFERENCE = 0.20   # share of bands dropped when the whole frame breaks up
GLITCH_BURST = 0.18         # seconds a break-up lasts
GLITCH_GAP = (4.0, 9.0)     # seconds of clean picture between break-ups
GLITCH_WINDOW = (60.0, 90.0)    # the stretch that breaks up now and then
PHOTO_FLASHES = (               # picture and the moment it flashes up
    ("a500full.png", 110.0),
    ("a500full.png", 116.0),
    ("c64full.png", 178.0),     # 2 min 58 s
)
GLITCH_PAD = 0.6            # break-up wrapped around each flash, so the photo
                            # looks like it arrived with the interference
CLEAR_GLIMPSE = 0.15        # mid-flash moment where the signal locks on and the
                            # photo is shown perfectly clean

SHOUT_DURATION = 2.0        # how long a shout stays up
SHOUT_WHITE = (255, 255, 255)
SHOUT_YELLOW = (255, 235, 60)
SHOUTS = (                  # thrown up by the first break-ups, in order
    ("OOPS !", SHOUT_YELLOW, (0.30, 0.32)),
    ("GLITCH !", SHOUT_WHITE, (0.68, 0.62)),
    ("GLITCH, AGAIN !", SHOUT_YELLOW, (0.42, 0.72)),
)


class CubeApp:
    def __init__(self, windowed=False, triggered=False):
        self.windowed = windowed
        self.triggered = triggered
        self.window_size = WINDOW_SIZE   # replaced by the real size in run()

        self.rotation_speed_x = 10
        self.rotation_speed_y = 18
        self.camera_y = 0.0
        self.camera_z = -6.0

        self.cube_offset = [0.0, 0.0, 0.0]
        self.second_cube_offset = [-3.0, 0.0, -5.0]  # left and back of the original

        text = ("     Retro computers such as the Commodore, Atari, ZX Spectrum, and Amiga played a pivotal role in shaping"
                " home computing and gaming.   These machines are remembered for their innovative features and their influence"
                " on the development of digital entertainment          ")
        self.caption1 = Caption(text)
        # Start fully off-screen to the right, then scroll left and wrap.
        self.caption_span = self.caption1.world_width / 2 + CAPTION_MARGIN
        self.caption_x = self.caption_span
        # Pace the single pass so it finishes exactly when the chiptune does.
        self.show_end = MUSIC_DURATION      # refined in run() from the real track
        self.caption_speed = 2 * self.caption_span / (self.show_end - CAPTION_START)

        self.elapsed = 0.0        # animation time, kept for blink_image
        self.blink_images = {}

        self.glitch = None        # needs the window size, so built in run()
        self.glitch_until = 0.0
        self.next_glitch = GLITCH_WINDOW[0]
        self.glitch_count = 0     # first few break-ups each get a shout
        self.shout = None
        self.shout_until = 0.0

        self.tunnel = TunnelEffect()
        self.amiga_ball = AmigaBall(radius = 1.5)
        self.atari_logo = AtariLogo(height=3.0)
        self.initial_zx_time = 150
        self.zx_logo = ZxLogo(self.initial_zx_time, height=2.5)
        self.c64_logo = C64Logo()

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

        if self.triggered:
            if not self._wait_for_click():
                pygame.quit()
                return
            global start_time      # restart the clock so the show begins on the click
            start_time = time.time()

        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()

        self.show_end = self._start_music()
        self.caption_speed = 2 * self.caption_span / (self.show_end - CAPTION_START)

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
        self.glitch = GlitchOverlay(self.window_size)
        self.caption1.prepare()   # pre-build now; avoids a freeze when the scroll starts

        prev_time = start_time

        running = True
        while running:
            now = time.time()
            t = now - start_time
            dt = now - prev_time
            prev_time = now
            self.elapsed = t

            running = self._handle_events(dt) and t < self.show_end + EXIT_DELAY

            surfaces = [gen.render(t) for gen in self.generators]
            self.cube.upload(surfaces)
            if 33 < t:
                self.second_cube.upload(surfaces)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0.0, self.camera_y, self.camera_z)

            self.procedure(dt, t)
            self._apply_scene_glitch()

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
        elif CAPTION_START < t:
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
        if 100 < t < 130:
            self.draw_amiga_ball(dt)
            if 110 < t < 120:
                self.amiga_ball.spin_speed += 0.5
            elif 120 < t < 130:
                self.amiga_ball.spin_speed -= 0.5
            if t > 115:
                self.amiga_ball.tilt += 1
        for filename, blink_at in PHOTO_FLASHES:
            self.blink_image(filename, blink_at)
        self._draw_shouts()
        if 130 < t < self.initial_zx_time:
            self.atari_logo.update(dt)
            self.atari_logo.render()
        if self.initial_zx_time < t < 165:
            self.zx_logo.update(dt, t)
            self.zx_logo.render()
        if 165 < t < 203:
            self.c64_logo.update(dt, t)
            self.c64_logo.render()
        if t > self.show_end - CREDITS_DURATION:
            self.overlay.draw_credits()

    def _start_shout(self):
        """Each of the first break-ups throws up its own caption."""
        self.glitch_count += 1
        if self.glitch_count <= len(SHOUTS):
            self.shout = SHOUTS[self.glitch_count - 1]
            self.shout_until = self.elapsed + SHOUT_DURATION

    def _wait_for_click(self):
        """Hold on a black screen until the window is clicked; False means quit."""
        glClear(GL_COLOR_BUFFER_BIT)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
            pygame.time.wait(10)

    def _draw_shouts(self):
        if self.shout and self.elapsed < self.shout_until:
            self.overlay.draw_shout(*self.shout)

    def _apply_scene_glitch(self):
        """The frame breaks up during GLITCH_WINDOW, and solidly around each
        Amiga flash so the photo looks like part of the interference."""
        if any(self._in_glimpse(at) for _, at in PHOTO_FLASHES):
            return                      # signal locked on; leave the frame alone

        if self._flashing_photo():
            self.glitch.apply(SCENE_INTERFERENCE)
            return

        if not GLITCH_WINDOW[0] <= self.elapsed < GLITCH_WINDOW[1]:
            return

        if self.elapsed >= self.glitch_until and self.elapsed >= self.next_glitch:
            self.glitch_until = self.elapsed + GLITCH_BURST
            self.next_glitch = self.glitch_until + random.uniform(*GLITCH_GAP)
            self._start_shout()

        if self.elapsed < self.glitch_until:
            self.glitch.apply(SCENE_INTERFERENCE)

    def _flashing_photo(self):
        return any(at - GLITCH_PAD <= self.elapsed < at + BLINK_DURATION + GLITCH_PAD
                   for _, at in PHOTO_FLASHES)

    def _in_glimpse(self, start_time):
        """The steady moment in the middle of a flash."""
        offset = (BLINK_DURATION - CLEAR_GLIMPSE) / 2
        return start_time + offset <= self.elapsed < start_time + offset + CLEAR_GLIMPSE

    def blink_image(self, filename, start_time, interference=BLINK_INTERFERENCE):
        """Show a picture full screen, fitted to the window, for BLINK_DURATION."""
        if not start_time <= self.elapsed < start_time + BLINK_DURATION:
            return

        image = self.blink_images.get(filename)
        if image is None:
            image = ScreenImage(os.path.join(ASSETS_DIR, filename))
            self.blink_images[filename] = image

        breaking_up = random.random() < GLITCH_CHANCE and not self._in_glimpse(start_time)
        image.draw(self.window_size, interference if breaking_up else 0.0)

    def _start_music(self):
        """Play the chiptune; returns when it will finish, in seconds from start_time."""
        if not os.path.exists(MUSIC_PATH):
            return MUSIC_DURATION

        duration = self._audible_length(pygame.mixer.Sound(MUSIC_PATH))
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play()
        return (time.time() - start_time) + duration

    def _audible_length(self, sound):
        """Track length without the trailing silence, so the show ends with the music."""
        magnitude = np.abs(pygame.sndarray.array(sound))
        if magnitude.ndim > 1:
            magnitude = magnitude.max(axis=1)

        audible = np.nonzero(magnitude > magnitude.max() * SILENCE_LEVEL)[0]
        if not len(audible):
            return sound.get_length()
        return (audible[-1] + 1) / pygame.mixer.get_init()[0]

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
            print(Cursor.POS(1, i+2) + Fore.CYAN + line, flush=True)
        print(Cursor.POS(1, len(INFO_LINES1) + 2)
              + Fore.RED + "elapsed:"
              + Fore.LIGHTWHITE_EX + f" {int(t) // 60:02d}:{int(t) % 60:02d}"
              + Style.RESET_ALL, end="", flush=True)

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
        if self.caption_x < -self.caption_span:   # one pass only, no wrap
            return

        self.caption_x -= self.caption_speed * dt

        glPushMatrix()
        glLoadIdentity()
        glTranslatef(self.caption_x, self.camera_y, CAPTION_Z)
        self.caption1.render()
        glPopMatrix()
