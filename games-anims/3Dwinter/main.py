import math
import os
import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT, KEYDOWN, K_ESCAPE, K_e
from OpenGL.GL import *
from OpenGL.GLU import *

from land import Land, FlattyLand
from tree import Tree
from snowman import Snowman
from snow import Snow
from igloo import Igloo
from patch import GroundPatch
from bonfire import Bonfire


class WinterScene:
    def __init__(self, width=1100, height=700):
        self.width = width
        self.height = height
        self.sky_color = (0.66, 0.76, 0.86)
        self.tree_positions = ((-8.0, -4.0), (-5.5, 3.0), (6.5, -6.0), (9.0, 2.5),
                               (-10.0, -9.0), (3.0, 8.0), (-2.0, -11.0), (11.0, -1.0),
                               (-12.0, -14.0), (1.0, 13.0), (-4.0, -14.0), (12.0, -12.0))
        self.clock = pygame.time.Clock()
        self.elapsed = 0.0
        self.sway_duration = 5.0
        self.travel_duration = 2.5
        self.settle_duration = 4.0
        self.enter_speed = 0.35
        self.entering = False
        self.entry_progress = 0.0
        self.entry_start_eye = (0.0, 0.0, 0.0)
        self._init_display()
        self._start_music()
        self._init_gl()
        self.land = Land(extent=80.0, resolution=144, seed=7)
        self.flatty_offset = (2.0 * self.land.extent, 0.0, 0.0)
        self.flatty_land = FlattyLand(extent=80.0, resolution=144, seed=11)
        self.trees = self._create_trees()
        self.snowman = Snowman(1.7, 0.0, self.land.surface_height(1.7, 0.0) - 0.6)
        self.igloo = Igloo(self.flatty_offset[0], self.flatty_offset[2],
                           self.flatty_land.surface_height(0.0, 0.0),
                           base_radius=3.5, layers_count=6)
        self.igloo_patch = GroundPatch(0.0, 0.0, self.igloo.base_radius * 4.0, self.flatty_land)
        self.bonfire = Bonfire(self.igloo.x, self.igloo.ground_height, self.igloo.z, scale=0.9)
        self.snow = Snow(220, (-22.0, 22.0, -20.0, 20.0, -1.5, 18.0))
        self.igloo_snow = Snow(200, (self.flatty_offset[0] - 22.0, self.flatty_offset[0] + 22.0,
                                     self.flatty_offset[2] - 20.0, self.flatty_offset[2] + 20.0,
                                     -1.5, 18.0), seed=123,
                               dome=(self.igloo.x, self.igloo.z, self.igloo.base_radius, self.igloo.ground_height))

    def _init_display(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Winter")

    def _start_music(self):
        music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dzisiaj.mp3")
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def _init_gl(self):
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_NORMALIZE)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 0.98, 0.92, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.35, 0.40, 0.48, 1.0))
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.35, 0.40, 0.48, 1.0))
        glClearColor(self.sky_color[0], self.sky_color[1], self.sky_color[2], 1.0)
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogfv(GL_FOG_COLOR, (self.sky_color[0], self.sky_color[1], self.sky_color[2], 1.0))
        glFogf(GL_FOG_START, 30.0)
        glFogf(GL_FOG_END, 80.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(55.0, self.width / self.height, 0.1, 220.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def _create_trees(self):
        trees = []
        for index, (x, z) in enumerate(self.tree_positions):
            ground = self.land.surface_height(x, z)
            trees.append(Tree(x, z, ground, snow_top=index % 3 != 0, seed=index + 1))
        return trees

    def _sway_eye(self, moment):
        orbit = math.radians(35.0 * math.sin(moment * 0.25))
        radius = 26.0
        return (math.sin(orbit) * radius, 10.0, math.cos(orbit) * radius)

    def _lerp(self, start, end, factor):
        return tuple(start[axis] + (end[axis] - start[axis]) * factor for axis in range(3))

    def _camera_eye_target(self):
        snowman_target = (0.0, 3.0, 0.0)
        if self.elapsed < self.sway_duration:
            return self._sway_eye(self.elapsed), snowman_target

        flatty_x, _, flatty_z = self.flatty_offset
        after_sway = self.elapsed - self.sway_duration
        progress = min(1.0, after_sway / self.travel_duration)
        eased = progress * progress * (3.0 - 2.0 * progress)
        settle = max(0.0, after_sway - self.travel_duration)

        eye_end = (flatty_x - 12.0 + math.sin(settle * 0.35) * 4.0,
                   8.0,
                   flatty_z + 15.0 + math.cos(settle * 0.35) * 2.0)
        target_end = (flatty_x, 2.5, flatty_z)
        eye = self._lerp(self._sway_eye(self.sway_duration), eye_end, eased)
        target = self._lerp(snowman_target, target_end, eased)
        return eye, target

    def _place_camera(self):
        if self.entering:
            eye, target = self.igloo.enter_igloo(self.entry_start_eye, self.entry_progress)
        else:
            eye, target = self._camera_eye_target()
        gluLookAt(eye[0], eye[1], eye[2], target[0], target[1], target[2], 0.0, 1.0, 0.0)

    def _start_entering(self):
        if not self.entering:
            self.entry_start_eye, _ = self._camera_eye_target()
            self.entry_progress = 0.0
            self.entering = True

    def _draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self._place_camera()
        glLightfv(GL_LIGHT0, GL_POSITION, (0.5, 1.0, 0.6, 0.0))
        self.land.draw()
        glPushMatrix()
        glTranslatef(*self.flatty_offset)
        self.flatty_land.draw()
        self.igloo_patch.draw()
        glPopMatrix()
        for tree in self.trees:
            tree.draw()
        self.snowman.draw()
        self.igloo.draw()
        self.bonfire.draw()
        self.snow.draw()
        self.igloo_snow.draw()

    def run(self):
        running = True
        while running:
            delta_seconds = self.clock.tick(60) / 1000.0
            self.elapsed += delta_seconds
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False
                elif event.type == KEYDOWN and event.key == K_e:
                    self._start_entering()
            if self.elapsed >= self.sway_duration + self.travel_duration + self.settle_duration:
                self._start_entering()
            if self.entering:
                self.entry_progress = min(1.0, self.entry_progress + self.enter_speed * delta_seconds)
            self.snow.update(delta_seconds)
            self.igloo_snow.update(delta_seconds)
            self.bonfire.update(delta_seconds)
            self._draw()
            pygame.display.flip()
        pygame.quit()


def main():
    WinterScene().run()


if __name__ == "__main__":
    main()
