import pygame
from pygame.locals import (DOUBLEBUF, KEYDOWN, K_ESCAPE, K_SPACE, K_p, MOUSEBUTTONDOWN,
                           MOUSEBUTTONUP, MOUSEMOTION, MOUSEWHEEL, OPENGL, QUIT)
from OpenGL.GL import (GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
                       GL_MODELVIEW, GL_PROJECTION, glClear, glClearColor, glEnable,
                       glLoadIdentity, glMatrixMode)
from OpenGL.GLU import gluPerspective


class BuildingApplication:
    def __init__(self, scene, window_width=1220, window_height=740,
                 background_color=(0.05, 0.06, 0.12), vertical_field_of_view=55.0,
                 window_title="Donut Headquarters Building"):
        self.scene = scene
        self.window_width = window_width
        self.window_height = window_height
        self.background_color = background_color
        self.vertical_field_of_view = vertical_field_of_view
        self.window_title = window_title
        self.building_movement_enabled = True
        self.is_dragging_orbit = False
        self.keep_running = True

    def initialize_display(self):
        pygame.init()
        pygame.display.set_mode((self.window_width, self.window_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(self.window_title)
        glEnable(GL_DEPTH_TEST)
        glClearColor(self.background_color[0], self.background_color[1], self.background_color[2], 1.0)
        self.configure_perspective_projection()

    def configure_perspective_projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.vertical_field_of_view, self.window_width / self.window_height, 0.5, 600.0)
        glMatrixMode(GL_MODELVIEW)

    def process_pending_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_running = False
            elif event.type == KEYDOWN:
                self.handle_key_press(event.key)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.is_dragging_orbit = True
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                self.is_dragging_orbit = False
            elif event.type == MOUSEMOTION and self.is_dragging_orbit:
                self.scene.camera.orbit_by(event.rel[0] * 0.01, -event.rel[1] * 0.01)
            elif event.type == MOUSEWHEEL:
                self.scene.camera.zoom_by(-event.y * 3.0)

    def handle_key_press(self, key_code):
        if key_code == K_ESCAPE:
            self.keep_running = False
        elif key_code == K_SPACE:
            self.building_movement_enabled = not self.building_movement_enabled
        elif key_code == K_p:
            self.scene.building.pillar_availability = not self.scene.building.pillar_availability

    def render_single_frame(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.scene.draw()
        pygame.display.flip()

    def run(self):
        self.initialize_display()
        frame_clock = pygame.time.Clock()
        while self.keep_running:
            elapsed_seconds = frame_clock.tick(60) / 1000.0
            self.process_pending_events()
            if self.building_movement_enabled:
                self.scene.update(elapsed_seconds)
            self.render_single_frame()
        pygame.quit()
